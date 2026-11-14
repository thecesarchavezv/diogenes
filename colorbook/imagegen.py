"""Único punto de salida de datos: el proveedor de imágenes.

COLORBOOK_IMAGE_PROVIDER elige el proveedor:
  openai     (por defecto) -> api.openai.com, con OPENAI_API_KEY
  higgsfield -> CLI `higgsfield` ya autenticado (higgsfield auth login)

Se envía: el prompt de texto y, si existen, las imágenes de referencia del usuario.
No se envía nada más. Con mock=True no hay ninguna llamada de red.
"""
from __future__ import annotations

import base64
import io
import math
import os
import random
import shlex
import subprocess
import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw

DEFAULT_MODEL = "gpt-image-1"


def size_for(trim: tuple[float, float]) -> str:
    w, h = trim
    ratio = w / h
    if ratio < 0.9:
        return "1024x1536"
    if ratio > 1.1:
        return "1536x1024"
    return "1024x1024"


def generate(prompt: str, size: str, refs: list[Path] | None = None, mock: bool = False,
             color: bool = False, seed: int = 0) -> Image.Image:
    if mock:
        return _mock(size, color, seed)
    refs = [r for r in (refs or []) if Path(r).exists()]
    if os.environ.get("COLORBOOK_IMAGE_PROVIDER", "openai") == "higgsfield":
        return _higgsfield(prompt, size, refs)
    try:
        from openai import OpenAI
    except ImportError as e:  # pragma: no cover
        raise SystemExit("Falta el paquete 'openai' (pip install -r requirements.txt) o usa --mock.") from e
    if not os.environ.get("OPENAI_API_KEY"):
        raise SystemExit("Falta OPENAI_API_KEY en el entorno (o usa --mock para probar sin API).")

    client = OpenAI()
    model = os.environ.get("COLORBOOK_IMAGE_MODEL", DEFAULT_MODEL)
    quality = os.environ.get("COLORBOOK_IMAGE_QUALITY", "medium")
    if refs:
        files = [open(r, "rb") for r in refs]
        try:
            result = client.images.edit(model=model, image=files, prompt=prompt, size=size, quality=quality)
        finally:
            for f in files:
                f.close()
    else:
        result = client.images.generate(model=model, prompt=prompt, size=size, quality=quality, n=1)
    return Image.open(io.BytesIO(base64.b64decode(result.data[0].b64_json))).convert("RGB")


def _higgsfield(prompt: str, size: str, refs: list[Path]) -> Image.Image:
    """Genera con el CLI de Higgsfield y descarga el resultado.

    COLORBOOK_HF_MODEL  modelo (z_image funciona en el plan gratuito; gpt_image_2_6 exige plan de pago)
    COLORBOOK_HF_PARAMS parámetros extra del modelo, p. ej. "--quality medium --resolution 2k"
    """
    model = os.environ.get("COLORBOOK_HF_MODEL", "z_image")
    w, h = (int(v) for v in size.split("x"))
    aspect = "3:4" if w < h else "4:3" if w > h else "1:1"
    cmd = ["higgsfield", "generate", "create", model, "--prompt", prompt, "--aspect-ratio", aspect,
           "--wait", "--wait-timeout", "8m", "--wait-interval", "10s"]
    cmd += shlex.split(os.environ.get("COLORBOOK_HF_PARAMS", ""))
    if refs and model != "z_image":  # z_image no admite imágenes de referencia
        for r in refs:
            cmd += ["--image-references", str(r)]
    done = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    urls = [t for t in done.stdout.split() if t.startswith("https://")]
    if done.returncode != 0 or not urls:
        raise RuntimeError(f"Higgsfield no devolvió imagen: {(done.stderr or done.stdout).strip()[-300:]}")
    with urllib.request.urlopen(urls[-1], timeout=120) as resp:
        return Image.open(io.BytesIO(resp.read())).convert("RGB")


def _mock(size: str, color: bool, seed: int) -> Image.Image:
    """Dibujo de relleno para probar el flujo completo sin gastar créditos."""
    w, h = (int(v) for v in size.split("x"))
    rng = random.Random(seed)
    img = Image.new("RGB", (w, h), (255, 240, 200) if color else "white")
    d = ImageDraw.Draw(img)
    palette = [(255, 120, 120), (120, 190, 255), (140, 220, 140), (255, 210, 90)]
    for i in range(7):
        cx, cy = rng.randint(180, w - 180), rng.randint(int(h * 0.38) if color else 180, h - 180)
        r = rng.randint(70, 150)
        fill = palette[i % 4] if color else None
        if i % 2:
            d.ellipse([cx - r, cy - r, cx + r, cy + r], outline="black", width=9, fill=fill)
        else:
            pts = []
            for k in range(10):
                rad = r if k % 2 == 0 else r * 0.45
                a = math.pi * k / 5 - math.pi / 2
                pts.append((cx + rad * math.cos(a), cy + rad * math.sin(a)))
            d.polygon(pts, outline="black", fill=fill, width=9)
    return img
