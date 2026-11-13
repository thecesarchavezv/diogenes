"""Limpieza a línea pura para imprenta y control de calidad automático."""
from __future__ import annotations

from PIL import Image, ImageChops, ImageOps, ImageStat

DPI = 300


def to_line_art(raw: Image.Image, target_in: tuple[float, float], threshold: int = 185) -> Image.Image:
    """Escala al área útil a 300 ppp y deja solo negro y blanco (bordes nítidos al imprimir)."""
    gray = ImageOps.autocontrast(raw.convert("L"), cutoff=1)
    box = (int(target_in[0] * DPI), int(target_in[1] * DPI))
    scale = min(box[0] / gray.width, box[1] / gray.height)
    gray = gray.resize((round(gray.width * scale), round(gray.height * scale)), Image.LANCZOS)
    return gray.point(lambda p: 255 if p > threshold else 0)


def quality_check(raw: Image.Image, processed: Image.Image) -> list[str]:
    """Devuelve avisos; lista vacía = página apta."""
    issues = []
    small = raw.convert("RGB").resize((256, 256))
    r, g, b = small.split()
    colorfulness = max(ImageStat.Stat(ImageChops.difference(r, g)).mean[0],
                       ImageStat.Stat(ImageChops.difference(g, b)).mean[0])
    if colorfulness > 6:
        issues.append("tiene color (debe ser solo línea negra)")
    hist = small.convert("L").histogram()
    midtones = sum(hist[70:190]) / (256 * 256)
    if midtones > 0.18:
        issues.append("tiene sombreado o grises")
    dark = processed.histogram()[0] / (processed.width * processed.height)
    if dark > 0.30:
        issues.append(f"demasiado relleno negro ({dark:.0%}); queda poco espacio para colorear")
    if dark < 0.01:
        issues.append("página casi vacía")
    return issues


def dominant_color(img: Image.Image) -> tuple[int, int, int]:
    return img.convert("RGB").resize((1, 1), Image.BOX).getpixel((0, 0))
