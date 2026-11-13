"""Construcción de prompts. Aquí vive la coherencia de estilo entre páginas."""
from __future__ import annotations

from .project import Project, load_config

LINE_ART_RULES = (
    "Black and white coloring book page. Clean black outlines on a pure white background. "
    "Line art only: no color, no gray, no shading, no gradients, no hatching, no solid black fills. "
    "Every shape is closed so it can be colored in. "
    "The whole subject sits inside the frame with an empty white margin on all four sides. "
    "No border, no frame, no watermark, no signature."
)
NO_TEXT = "No text, no letters, no numbers anywhere in the image."


def page_prompt(project: Project, page: dict) -> str:
    d = project.data
    audience = load_config("audiences")[d["audience"]]["style"]
    parts = [LINE_ART_RULES, f"Line style: {audience}."]
    if d.get("style_lock"):
        parts.append(f"Book style (keep identical on every page): {d['style_lock']}.")
    if d.get("characters"):
        cast = " ".join(f"{c['name']}: {c['description']}." for c in d["characters"])
        parts.append(f"Recurring characters, always drawn exactly like this: {cast}")
    if d.get("references"):
        parts.append("Match the drawing style of the reference image(s); do not copy their content.")
    parts.append(f"Scene: {page['prompt']}.")
    for note in page.get("notes", []):
        parts.append(f"Correction requested: {note}.")
    in_image_text = d.get("text_mode") == "in_image" and page.get("caption")
    if in_image_text:
        parts.append(
            f'Include this exact short text in large, clear, outlined hand-lettering at the bottom: "{page["caption"]}".'
        )
    else:
        parts.append(NO_TEXT)
    return " ".join(parts)


def character_sheet_prompt(project: Project) -> str:
    d = project.data
    audience = load_config("audiences")[d["audience"]]["style"]
    cast = " ".join(f"{c['name']}: {c['description']}." for c in d["characters"])
    return (
        f"{LINE_ART_RULES} Line style: {audience}. "
        f"Character reference sheet showing each character once, full body, standing, neutral pose, side by side: {cast} "
        f"{'Book style: ' + d['style_lock'] + '. ' if d.get('style_lock') else ''}{NO_TEXT}"
    )


def cover_prompt(project: Project) -> str:
    d = project.data
    cover = d.setdefault("cover", {})
    scene = cover.get("prompt") or f"a cheerful scene that represents the theme: {d.get('theme', d['title'])}"
    parts = [
        "Full-color children's book cover illustration." if d["audience"] != "adults"
        else "Full-color cover illustration for an adult coloring book.",
        "Bold black outlines in the same line-art style as the interior pages, filled with bright flat colors.",
        f"Scene: {scene}.",
        "Leave the top third of the image calm and uncluttered so a title can be placed there.",
        "No text, no letters, no logos.",
    ]
    if d.get("style_lock"):
        parts.append(f"Style: {d['style_lock']}.")
    if d.get("characters"):
        parts.append("Characters: " + " ".join(f"{c['name']}: {c['description']}." for c in d["characters"]))
    for note in cover.get("notes", []):
        parts.append(f"Correction requested: {note}.")
    return " ".join(parts)
