"""CLI que usa el agente. Cada comando imprime JSON para que el LLM lo lea sin ambigüedad.

  python -m colorbook init     <dir> --title ... --mode ... --audience ... --platform ...
  python -m colorbook plan     <dir> --file plan.json
  python -m colorbook generate <dir> [--pages 1,2,3 | --pending] [--mock]
  python -m colorbook revise   <dir> --page 3 --note "líneas más gruesas" [--mock]
  python -m colorbook cover    <dir> [--note ...] [--mock]
  python -m colorbook prompts  <dir>
  python -m colorbook import   <dir> --page 3 --file dibujo.png   (o --cover)
  python -m colorbook status   <dir>
  python -m colorbook build    <dir>
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from PIL import Image

from . import imagegen, pdf, postprocess, prompts
from .project import MODES, Project, load_config, parse_trim, slugify


def out(obj) -> None:
    print(json.dumps(obj, indent=2, ensure_ascii=False))


def cmd_init(a) -> None:
    platforms = load_config("platforms")
    plat = platforms[a.platform]
    trim = a.trim or plat["default_trim"]
    parse_trim(trim)
    if trim not in plat["trims"]:
        print(f"Aviso: {trim} no está en la lista habitual de {plat['label']}: {plat['trims']}", file=sys.stderr)
    data = {
        "title": a.title, "subtitle": a.subtitle or "", "author": a.author or "",
        "mode": a.mode, "audience": a.audience, "theme": a.theme or a.title,
        "platform": a.platform, "trim": trim, "paper": a.paper,
        "single_sided": not a.double_sided,
        "text_mode": "typeset", "style_lock": "", "characters": [], "references": [],
        "pages": [], "cover": {"title_mode": "typeset"},
    }
    directory = Path(a.dir) if a.dir else Path("projects") / slugify(a.title)
    project = Project.create(directory, data)
    for ref in a.reference or []:
        dest = project.dir / "refs" / Path(ref).name
        shutil.copy(ref, dest)
        project.data["references"].append(str(dest.relative_to(project.dir)))
    project.save()
    out({"project": str(project.dir), "platform": plat["label"], "trim": trim,
         "verify_specs": plat.get("verify", False)})


def cmd_plan(a) -> None:
    """Fusiona el plan escrito por el agente: estilo, personajes, páginas y portada."""
    project = Project(a.dir)
    plan = json.loads(Path(a.file).read_text(encoding="utf-8"))
    d = project.data
    for key in ("style_lock", "characters", "text_mode", "subtitle", "copyright"):
        if key in plan:
            d[key] = plan[key]
    if "cover" in plan:
        d["cover"].update(plan["cover"])
    if "pages" in plan:
        if a.replace:
            d["pages"] = []
        start = len(d["pages"])
        for i, p in enumerate(plan["pages"], start=start + 1):
            d["pages"].append({"n": i, "prompt": p["prompt"], "caption": p.get("caption", ""),
                               "status": "pending", "version": 0, "notes": []})
    project.save()
    out({"pages_planned": len(d["pages"]), "style_lock": d["style_lock"],
         "characters": [c["name"] for c in d["characters"]]})


def _refs(project: Project, mock: bool) -> list[Path]:
    """Referencias del usuario + hoja de personajes (se crea una vez, en modo cuento)."""
    d = project.data
    if mock:
        return []
    if d["mode"] == "storybook" and d.get("characters") and not d.get("character_sheet"):
        img = imagegen.generate(prompts.character_sheet_prompt(project), "1536x1024",
                                [project.abs(r) for r in d["references"]])
        img.save(project.abs("refs/characters.png"))
        d["character_sheet"] = "refs/characters.png"
        project.save()
    refs = [project.abs(r) for r in d["references"]]
    if d.get("character_sheet"):
        refs.append(project.abs(d["character_sheet"]))
    return refs


def _render_page(project: Project, page: dict, refs: list[Path], mock: bool) -> dict:
    tw, th = project.trim
    version = page["version"] + 1
    try:
        raw = imagegen.generate(prompts.page_prompt(project, page), imagegen.size_for((tw, th)),
                                refs, mock=mock, seed=page["n"] * 100 + version)
    except SystemExit:
        raise
    except Exception as e:  # una página fallida no tumba el lote
        page["status"] = "failed"
        return {"n": page["n"], "status": "failed", "error": str(e)[:300]}
    return _store_page(project, page, raw, version)


def _store_page(project: Project, page: dict, raw: Image.Image, version: int) -> dict:
    """Guarda el original, lo limpia a línea pura y pasa el control de calidad."""
    tw, th = project.trim
    raw_rel = f"pages/raw/page_{page['n']:03d}_v{version}.png"
    rel = f"pages/page_{page['n']:03d}.png"
    raw.save(project.abs(raw_rel))
    clean = postprocess.to_line_art(raw, (tw - 1.0, th - 1.0 - (pdf.CAPTION_H if page.get("caption") else 0)))
    clean.save(project.abs(rel))
    issues = postprocess.quality_check(raw, clean)
    page.update(version=version, file=rel, raw=raw_rel, issues=issues,
                status="needs_review" if issues else "done")
    return {"n": page["n"], "status": page["status"], "file": str(project.abs(rel)), "issues": issues}


def _select(project: Project, a) -> list[dict]:
    if getattr(a, "pages", None):
        return [project.page(int(n)) for n in a.pages.split(",")]
    return [p for p in project.pages if p["status"] in ("pending", "failed")]


def cmd_generate(a) -> None:
    project = Project(a.dir)
    todo = _select(project, a)
    refs = _refs(project, a.mock)
    with ThreadPoolExecutor(max_workers=a.workers) as pool:
        results = list(pool.map(lambda p: _render_page(project, p, refs, a.mock), todo))
    project.save()
    out({"generated": results, "mock": a.mock})


def cmd_revise(a) -> None:
    project = Project(a.dir)
    page = project.page(a.page)
    if a.prompt:
        page["prompt"] = a.prompt
    if a.caption is not None:
        page["caption"] = a.caption
    if a.note:
        page.setdefault("notes", []).append(a.note)
    result = _render_page(project, page, _refs(project, a.mock), a.mock)
    project.save()
    out(result)


def cmd_style(a) -> None:
    """Fija el estilo aprobado. Las páginas ya hechas con otro estilo vuelven a 'pending'."""
    project = Project(a.dir)
    project.data["style_lock"] = a.set
    if a.redo:
        for p in project.pages:
            p["status"] = "pending"
    project.save()
    out({"style_lock": a.set, "pending": sum(p["status"] == "pending" for p in project.pages)})


def cmd_import(a) -> None:
    """Incorpora una imagen hecha fuera (otro generador o un dibujo propio) como página o portada."""
    project = Project(a.dir)
    img = Image.open(a.file).convert("RGB")
    if a.cover:
        result = _store_cover(project, img)
    else:
        page = project.page(a.page)
        result = _store_page(project, page, img, page["version"] + 1)
    project.save()
    out(result)


def cmd_prompts(a) -> None:
    """Muestra los prompts exactos, para generar las imágenes con otra herramienta."""
    project = Project(a.dir)
    out({"pages": [{"n": p["n"], "prompt": prompts.page_prompt(project, p)} for p in project.pages],
         "cover": prompts.cover_prompt(project)})


def cmd_cover(a) -> None:
    project = Project(a.dir)
    cover = project.data["cover"]
    if a.prompt:
        cover["prompt"] = a.prompt
    if a.blurb:
        cover["blurb"] = a.blurb
    if a.note:
        cover.setdefault("notes", []).append(a.note)
    img = imagegen.generate(prompts.cover_prompt(project), imagegen.size_for(project.trim),
                            _refs(project, a.mock), mock=a.mock, color=True,
                            seed=cover.get("version", 0) + 1)
    result = _store_cover(project, img)
    project.save()
    out({**result, "mock": a.mock})


def _store_cover(project: Project, img: Image.Image) -> dict:
    """Recorta la ilustración al panel de portada con su sangrado, a 300 ppp."""
    cover = project.data["cover"]
    version = cover.get("version", 0) + 1
    tw, th = project.trim
    bleed = project.platform["bleed"]
    px = (round((tw + bleed) * 300), round((th + 2 * bleed) * 300))
    scale = max(px[0] / img.width, px[1] / img.height)
    img = img.resize((round(img.width * scale), round(img.height * scale)), Image.LANCZOS)
    left, top = (img.width - px[0]) // 2, (img.height - px[1]) // 2
    img.crop((left, top, left + px[0], top + px[1])).save(project.abs("cover/front.png"))
    cover.update(file="cover/front.png", version=version)
    return {"cover": str(project.abs("cover/front.png")), "version": version}


def cmd_status(a) -> None:
    project = Project(a.dir)
    d = project.data
    counts: dict[str, int] = {}
    for p in project.pages:
        counts[p["status"]] = counts.get(p["status"], 0) + 1
    out({"title": d["title"], "mode": d["mode"], "platform": d["platform"], "trim": d["trim"],
         "style_locked": bool(d["style_lock"]), "pages": counts,
         "needs_review": [{"n": p["n"], "issues": p["issues"]} for p in project.pages if p.get("issues")],
         "cover_ready": bool(d["cover"].get("file"))})


def cmd_build(a) -> None:
    project = Project(a.dir)
    d, plat = project.data, project.platform
    not_ready = [p["n"] for p in project.pages if not p.get("file")]
    if not_ready and not a.force:
        raise SystemExit(f"Faltan páginas por generar: {not_ready} (usa --force para omitirlas)")
    slug = slugify(d["title"])
    interior = project.abs(f"output/{slug}-interior.pdf")
    report = {"interior": str(interior), **pdf.build_interior(project, interior)}
    warnings = []
    if plat["kind"] == "print":
        if report["padding_blank_pages"] > 2:
            warnings.append(f"Hay {report['padding_blank_pages']} páginas en blanco al final para llegar al mínimo de "
                            f"{plat['min_pages']} de {plat['label']}: conviene añadir más ilustraciones")
        max_pages = (plat.get("max_pages_by_trim", {}).get(d["trim"], {}).get(d.get("paper", "white"))
                     or plat["max_pages"])
        if report["pages"] > max_pages:
            warnings.append(f"Supera el máximo de {max_pages} páginas de {plat['label']} para {d['trim']}")
        if d["cover"].get("file"):
            cover = project.abs(f"output/{slug}-cubierta.pdf")
            report["cover"] = {"file": str(cover), **pdf.build_cover(project, cover, report["pages"])}
        else:
            warnings.append("No hay portada: ejecuta 'cover' para generar el PDF de cubierta")
        if plat.get("verify"):
            warnings.append(f"Confirma lomo y márgenes con la plantilla oficial de {plat['label']} antes de subir")
    report["warnings"] = warnings
    out(report)


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(prog="colorbook", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("init")
    p.add_argument("dir", nargs="?")
    p.add_argument("--title", required=True)
    p.add_argument("--subtitle")
    p.add_argument("--author")
    p.add_argument("--theme")
    p.add_argument("--mode", choices=MODES, default="standard")
    p.add_argument("--audience", choices=list(load_config("audiences")), default="kids_4_8")
    p.add_argument("--platform", choices=[k for k in load_config("platforms") if not k.startswith("_")],
                   default="personal")
    p.add_argument("--trim")
    p.add_argument("--paper", choices=["white", "cream"], default="white")
    p.add_argument("--double-sided", action="store_true", help="imprime dibujos por ambas caras")
    p.add_argument("--reference", action="append", help="imagen de referencia de estilo (repetible)")
    p.set_defaults(fn=cmd_init)

    p = sub.add_parser("plan")
    p.add_argument("dir")
    p.add_argument("--file", required=True)
    p.add_argument("--replace", action="store_true")
    p.set_defaults(fn=cmd_plan)

    p = sub.add_parser("generate")
    p.add_argument("dir")
    p.add_argument("--pages", help="p. ej. 1,2,3 (por defecto: pendientes y fallidas)")
    p.add_argument("--workers", type=int, default=4)
    p.add_argument("--mock", action="store_true")
    p.set_defaults(fn=cmd_generate)

    p = sub.add_parser("revise")
    p.add_argument("dir")
    p.add_argument("--page", type=int, required=True)
    p.add_argument("--note")
    p.add_argument("--prompt")
    p.add_argument("--caption")
    p.add_argument("--mock", action="store_true")
    p.set_defaults(fn=cmd_revise)

    p = sub.add_parser("style")
    p.add_argument("dir")
    p.add_argument("--set", required=True)
    p.add_argument("--redo", action="store_true", help="regenerar todo con el estilo nuevo")
    p.set_defaults(fn=cmd_style)

    p = sub.add_parser("cover")
    p.add_argument("dir")
    p.add_argument("--prompt")
    p.add_argument("--blurb")
    p.add_argument("--note")
    p.add_argument("--mock", action="store_true")
    p.set_defaults(fn=cmd_cover)

    p = sub.add_parser("import")
    p.add_argument("dir")
    p.add_argument("--file", required=True)
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--page", type=int)
    g.add_argument("--cover", action="store_true")
    p.set_defaults(fn=cmd_import)

    p = sub.add_parser("prompts")
    p.add_argument("dir")
    p.set_defaults(fn=cmd_prompts)

    p = sub.add_parser("status")
    p.add_argument("dir")
    p.set_defaults(fn=cmd_status)

    p = sub.add_parser("build")
    p.add_argument("dir")
    p.add_argument("--force", action="store_true")
    p.set_defaults(fn=cmd_build)

    a = ap.parse_args(argv)
    a.fn(a)
