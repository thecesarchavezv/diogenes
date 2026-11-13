"""Maquetación: PDF interior y PDF de cubierta (contraportada + lomo + portada)."""
from __future__ import annotations

from pathlib import Path

from PIL import Image
from reportlab.lib.colors import Color, black, white
from reportlab.lib.utils import ImageReader, simpleSplit
from reportlab.pdfgen import canvas

from .postprocess import dominant_color
from .project import Project, gutter_for, spine_width

IN = 72.0
FONT, FONT_BOLD = "Helvetica", "Helvetica-Bold"
CAPTION_H = 1.2  # pulgadas reservadas para el texto del cuento


def _fit_text(c, text, font, max_size, width, max_lines=3):
    """Mayor tamaño de letra con el que el texto cabe en `width` y `max_lines`."""
    size = max_size
    while size > 10:
        lines = simpleSplit(text, font, size, width)
        if len(lines) <= max_lines:
            return size, lines
        size -= 2
    return size, simpleSplit(text, font, size, width)


def _centered(c, lines, font, size, cx, top_y, leading=1.2):
    c.setFont(font, size)
    for i, line in enumerate(lines):
        c.drawCentredString(cx, top_y - size - i * size * leading, line)


def plan_interior(project: Project) -> list[dict]:
    """Secuencia final de páginas, ya con portadilla, reversos en blanco y relleno."""
    d, plat = project.data, project.platform
    is_print = plat["kind"] == "print"
    seq: list[dict] = []
    if not is_print and d.get("cover", {}).get("file"):
        seq.append({"type": "cover"})
    if d.get("front_matter", True):
        seq.append({"type": "title"})
        if is_print:
            seq.append({"type": "copyright"})
    for p in project.pages:
        if not p.get("file"):
            continue
        # En imprenta las ilustraciones van en página impar (derecha).
        if is_print and d.get("single_sided", True) and len(seq) % 2 == 1:
            seq.append({"type": "blank"})
        seq.append({"type": "image", "page": p})
    if is_print:
        while len(seq) < plat["min_pages"] or len(seq) % 2:
            seq.append({"type": "blank"})
    return seq


def build_interior(project: Project, out: Path) -> dict:
    d, plat = project.data, project.platform
    tw, th = project.trim
    seq = plan_interior(project)
    is_print = plat["kind"] == "print"
    gutter = gutter_for(plat, len(seq)) if is_print else plat["outside_margin"]
    outside = plat["outside_margin"]
    storybook = d["mode"] == "storybook" and d.get("text_mode", "typeset") == "typeset"

    c = canvas.Canvas(str(out), pagesize=(tw * IN, th * IN))
    c.setTitle(d["title"])
    c.setAuthor(d.get("author", ""))
    for i, item in enumerate(seq):
        recto = i % 2 == 0  # página 1 = derecha
        left = (gutter if recto else outside) if is_print else outside
        right = (outside if recto else gutter) if is_print else outside
        x0, y0 = left * IN, outside * IN
        w, h = (tw - left - right) * IN, (th - 2 * outside) * IN
        cx = x0 + w / 2

        if item["type"] == "cover":
            c.drawImage(ImageReader(str(project.abs(d["cover"]["file"]))), 0, 0, tw * IN, th * IN,
                        preserveAspectRatio=True, anchor="c")
            _cover_title(c, d, 0, 0, tw * IN, th * IN)
        elif item["type"] == "title":
            size, lines = _fit_text(c, d["title"], FONT_BOLD, 44, w)
            _centered(c, lines, FONT_BOLD, size, cx, y0 + h * 0.68)
            if d.get("subtitle"):
                _centered(c, simpleSplit(d["subtitle"], FONT, 18, w), FONT, 18, cx, y0 + h * 0.45)
            if d.get("author"):
                _centered(c, [d["author"]], FONT, 16, cx, y0 + h * 0.2)
        elif item["type"] == "copyright":
            text = d.get("copyright") or f"© {d.get('author', '')}. Todos los derechos reservados."
            c.setFont(FONT, 9)
            for k, line in enumerate(simpleSplit(text, FONT, 9, w)):
                c.drawString(x0, y0 + 60 - k * 12, line)
        elif item["type"] == "image":
            p = item["page"]
            cap_h = CAPTION_H * IN if storybook and p.get("caption") else 0
            c.drawImage(ImageReader(str(project.abs(p["file"]))), x0, y0 + cap_h, w, h - cap_h,
                        preserveAspectRatio=True, anchor="c")
            if cap_h:
                size, lines = _fit_text(c, p["caption"], FONT_BOLD, 20, w, max_lines=3)
                _centered(c, lines, FONT_BOLD, size, cx, y0 + cap_h - 6)
        c.showPage()
    c.save()
    padding = 0
    while padding < len(seq) and seq[-1 - padding]["type"] == "blank":
        padding += 1
    return {"pages": len(seq), "illustrations": sum(1 for s in seq if s["type"] == "image"),
            "padding_blank_pages": padding, "gutter_in": gutter, "trim_in": [tw, th]}


def _cover_title(c, d, x, y, w, h):
    """Título tipografiado sobre una banda blanca: ortografía y acentos siempre correctos."""
    if d.get("cover", {}).get("title_mode", "typeset") != "typeset":
        return
    band_w = w * 0.86
    size, lines = _fit_text(c, d["title"], FONT_BOLD, 46, band_w - 30, max_lines=2)
    band_h = len(lines) * size * 1.2 + 26
    bx, by = x + (w - band_w) / 2, y + h * 0.9 - band_h
    c.setFillColor(Color(1, 1, 1, alpha=0.93))
    c.setStrokeColor(black)
    c.setLineWidth(2.5)
    c.roundRect(bx, by, band_w, band_h, 14, fill=1, stroke=1)
    c.setFillColor(black)
    _centered(c, lines, FONT_BOLD, size, x + w / 2, by + band_h - 9)
    if d.get("author"):
        c.setFillColor(Color(1, 1, 1, alpha=0.9))
        aw = c.stringWidth(d["author"], FONT_BOLD, 15) + 24
        c.roundRect(x + (w - aw) / 2, y + h * 0.06, aw, 26, 8, fill=1, stroke=0)
        c.setFillColor(black)
        c.setFont(FONT_BOLD, 15)
        c.drawCentredString(x + w / 2, y + h * 0.06 + 8, d["author"])


def build_cover(project: Project, out: Path, page_count: int) -> dict:
    """Cubierta completa en una sola página: contraportada | lomo | portada, con sangrado."""
    d, plat = project.data, project.platform
    tw, th = project.trim
    bleed = plat["bleed"]
    spine = spine_width(plat, page_count, d.get("paper", "white"))
    W, H = (2 * tw + spine + 2 * bleed) * IN, (th + 2 * bleed) * IN
    art = Image.open(project.abs(d["cover"]["file"]))
    r, g, b = dominant_color(art)
    ink = black if (0.299 * r + 0.587 * g + 0.114 * b) > 140 else white

    c = canvas.Canvas(str(out), pagesize=(W, H))
    c.setFillColorRGB(r / 255, g / 255, b / 255)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    # Portada: la ilustración cubre el panel y su sangrado (recorte tipo "cover").
    fx, fw = (bleed + tw + spine) * IN, (tw + bleed) * IN
    scale = max(fw / art.width, H / art.height)
    iw, ih = art.width * scale, art.height * scale
    c.saveState()
    clip = c.beginPath()
    clip.rect(fx, 0, fw, H)
    c.clipPath(clip, stroke=0)
    c.drawImage(ImageReader(art), fx + (fw - iw) / 2, (H - ih) / 2, iw, ih)
    c.restoreState()
    _cover_title(c, d, fx, bleed * IN, tw * IN, th * IN)

    # Contraportada: texto de venta y zona blanca para el código de barras.
    bx, safe = bleed * IN, 0.5 * IN
    c.setFillColor(ink)
    blurb = d.get("cover", {}).get("blurb", "")
    if blurb:
        c.setFont(FONT, 16)
        for k, line in enumerate(simpleSplit(blurb, FONT, 16, tw * IN - 2 * safe)):
            c.drawString(bx + safe, H - bleed * IN - safe - 16 - k * 22, line)
    if plat.get("barcode_zone"):
        zw, zh = (v * IN for v in plat["barcode_zone"])
        c.setFillColor(white)
        c.rect(bx + tw * IN - zw - 0.25 * IN, (bleed + 0.25) * IN, zw, zh, fill=1, stroke=0)

    # Lomo: solo lleva texto si el libro es lo bastante grueso.
    spine_text = page_count >= plat["spine_text_min_pages"]
    if spine_text:
        c.saveState()
        c.translate((bleed + tw) * IN + spine * IN / 2, H / 2)
        c.rotate(-90)
        size = min(12, spine * IN * 0.5)
        c.setFillColor(ink)
        c.setFont(FONT_BOLD, size)
        c.drawCentredString(0, -size / 3, d["title"])
        c.restoreState()
    c.showPage()
    c.save()
    return {"spine_in": round(spine, 4), "size_in": [round(W / IN, 3), round(H / IN, 3)],
            "spine_text": spine_text}
