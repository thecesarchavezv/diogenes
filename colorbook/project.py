"""Estado del libro (book.json) y reglas de cada plataforma."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "config"

NAMED_TRIMS = {"A4": (8.27, 11.69), "A5": (5.83, 8.27)}
MODES = ("standard", "publishing", "storybook")


def load_config(name: str) -> dict:
    return json.loads((CONFIG / f"{name}.json").read_text(encoding="utf-8"))


def parse_trim(trim: str) -> tuple[float, float]:
    """'8.5x11' -> (8.5, 11.0) en pulgadas."""
    if trim.upper() in NAMED_TRIMS:
        return NAMED_TRIMS[trim.upper()]
    m = re.fullmatch(r"\s*([\d.]+)\s*[xX]\s*([\d.]+)\s*", trim)
    if not m:
        raise ValueError(f"Tamaño no reconocido: {trim!r} (usa p. ej. 8.5x11 o A4)")
    return float(m.group(1)), float(m.group(2))


def slugify(text: str) -> str:
    text = re.sub(r"[^\w\s-]", "", text.lower(), flags=re.UNICODE)
    return re.sub(r"[\s_-]+", "-", text).strip("-") or "libro"


class Project:
    """Carpeta de un libro: book.json + pages/ + cover/ + output/."""

    def __init__(self, path: str | Path):
        self.dir = Path(path)
        self.file = self.dir / "book.json"
        if not self.file.exists():
            raise FileNotFoundError(f"No existe {self.file}. Ejecuta primero 'init'.")
        self.data = json.loads(self.file.read_text(encoding="utf-8"))

    @classmethod
    def create(cls, path: str | Path, data: dict) -> "Project":
        d = Path(path)
        for sub in ("pages/raw", "cover", "output", "refs"):
            (d / sub).mkdir(parents=True, exist_ok=True)
        (d / "book.json").write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        return cls(d)

    def save(self) -> None:
        self.file.write_text(json.dumps(self.data, indent=2, ensure_ascii=False), encoding="utf-8")

    # --- acceso cómodo -------------------------------------------------
    @property
    def pages(self) -> list[dict]:
        return self.data.setdefault("pages", [])

    def page(self, n: int) -> dict:
        for p in self.pages:
            if p["n"] == n:
                return p
        raise KeyError(f"No existe la página {n}")

    @property
    def platform(self) -> dict:
        return load_config("platforms")[self.data["platform"]]

    @property
    def trim(self) -> tuple[float, float]:
        return parse_trim(self.data["trim"])

    def abs(self, rel: str) -> Path:
        return self.dir / rel


def gutter_for(platform: dict, page_count: int) -> float:
    for limit, gutter in platform["gutter_by_pages"]:
        if page_count <= limit:
            return gutter
    return platform["gutter_by_pages"][-1][1]


def spine_width(platform: dict, page_count: int, paper: str = "white") -> float:
    per_page = platform["spine_per_page"].get(paper, platform["spine_per_page"]["white"])
    return page_count * per_page + platform.get("spine_offset", 0.0)
