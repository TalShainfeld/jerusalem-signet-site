import json
import os
from jinja2 import Environment, FileSystemLoader
from PIL import Image, ImageDraw, ImageFont

FONT_TITLE = "assets/fonts/PlayfairDisplay-Bold.ttf"
FONT_BODY = "assets/fonts/Montserrat-Regular.ttf"
BG_IMAGE = "assets/images/templates/Galil_View.jfif"
OUTPUT_PINS = "assets/images/pinterest/"
PINTEREST_UPLOAD_ROOT = "pinterest_upload"
CONTENT_JSON = "content.json"
PINTEREST_TEMPLATE = "pinterest_landing.html.j2"


def _asset_href_for_pinterest_landing(relative_path: str) -> str:
    """Resolve repo-relative asset paths for HTML files under pinterest_upload/<id>/."""
    rel = (relative_path or "").lstrip("/").replace("\\", "/")
    if not rel:
        return ""
    return "../../" + rel


def _display_title(raw: dict) -> str:
    if raw.get("title"):
        return str(raw["title"])
    if raw.get("english_name"):
        return str(raw["english_name"])
    if raw.get("name"):
        return str(raw["name"])
    return str(raw.get("id", ""))


def flatten_content_paragraphs(raw: dict) -> list[str]:
    """Collect all narrative blocks from content.json into ordered plain-text paragraphs."""
    out: list[str] = []

    intro = raw.get("intro")
    if isinstance(intro, str) and intro.strip():
        out.append(intro.strip())

    symbols = raw.get("symbols")
    if isinstance(symbols, list):
        for sym in symbols:
            if not isinstance(sym, dict):
                continue
            he = sym.get("hebrew", "")
            lab = sym.get("label", "")
            if he and lab:
                out.append(f"{he} — {lab}")
            elif he or lab:
                out.append(f"{he}{lab}".strip())

    pardes = raw.get("pardes")
    if isinstance(pardes, dict):
        layers = pardes.get("layers")
        if isinstance(layers, list):
            for layer in layers:
                if not isinstance(layer, dict):
                    continue
                label = layer.get("label", "")
                subtitle = layer.get("subtitle", "")
                desc = layer.get("description", "")
                head = f"{label} ({subtitle})" if label and subtitle else (label or subtitle)
                if head and desc:
                    out.append(f"{head}: {desc}")
                elif desc:
                    out.append(desc)
                elif head:
                    out.append(head)

    for section in raw.get("sections") or []:
        if not isinstance(section, dict):
            continue
        stype = section.get("type")
        if stype == "callout":
            t = section.get("text")
            if isinstance(t, str) and t.strip():
                out.append(t.strip())
        elif stype == "paragraphs":
            for line in section.get("items") or []:
                if isinstance(line, str) and line.strip():
                    out.append(line.strip())
        elif stype == "quote":
            t = section.get("text")
            if isinstance(t, str) and t.strip():
                out.append(t.strip())
        elif stype == "reference":
            t = section.get("text")
            if isinstance(t, str) and t.strip():
                out.append(t.strip())
        elif stype == "subsections":
            for sub in section.get("items") or []:
                if not isinstance(sub, dict):
                    continue
                st = sub.get("title", "")
                sx = sub.get("text", "")
                if st and sx:
                    out.append(f"{st}: {sx}")
                elif sx:
                    out.append(str(sx).strip())
                elif st:
                    out.append(str(st).strip())

    for story in raw.get("stories") or []:
        if not isinstance(story, dict):
            continue
        st = story.get("title", "")
        sx = story.get("text", "")
        if st and sx:
            out.append(f"{st}: {sx}")
        elif sx:
            out.append(str(sx).strip())
        elif st:
            out.append(str(st).strip())

    for sub in raw.get("subsections") or []:
        if not isinstance(sub, dict):
            continue
        nm = sub.get("name", "")
        hn = sub.get("hebrew_name", "")
        head = f"{nm} ({hn})" if nm and hn else (nm or hn)
        vh = sub.get("verse_he", "")
        ve = sub.get("verse_en", "")
        if head:
            out.append(head)
        if isinstance(vh, str) and vh.strip():
            out.append(vh.strip())
        if isinstance(ve, str) and ve.strip():
            out.append(ve.strip())

    return out


def build_pinterest_item(raw: dict) -> dict:
    """Shape one content.json entry for pinterest_landing.html.j2 (item.*)."""
    icon_path = raw.get("icon") or ""
    return {
        "id": raw.get("id", ""),
        "icon": _asset_href_for_pinterest_landing(icon_path),
        "title": _display_title(raw),
        "verse_he": (raw.get("verse_he") or "").strip(),
        "verse_en": (raw.get("verse_en") or "").strip(),
        "content": flatten_content_paragraphs(raw),
    }


def create_pinterest_pin(item_id, title, subtitle="Ancient Wisdom"):
    """Render a Pinterest JPEG pin using the Galil template background."""
    if not os.path.exists(OUTPUT_PINS):
        os.makedirs(OUTPUT_PINS)

    try:
        img = Image.open(BG_IMAGE).convert("RGBA")
        width, height = img.size

        overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        draw.rectangle([0, 0, width, height], fill=(0, 0, 0, 100))

        font_t = ImageFont.truetype(FONT_TITLE, 80)
        font_s = ImageFont.truetype(FONT_BODY, 30)

        draw.text((width // 2, height // 2 - 50), title, fill=(212, 175, 55), font=font_t, anchor="mm")
        draw.text((width // 2, height // 2 + 50), subtitle, fill=(255, 255, 255), font=font_s, anchor="mm")

        combined = Image.alpha_composite(img, overlay)
        final_pin = combined.convert("RGB")
        pin_path = os.path.join(OUTPUT_PINS, f"pin_{item_id}.jpg")
        final_pin.save(pin_path, quality=95)
        return pin_path
    except Exception as e:
        print(f"Error creating pin for {item_id}: {e}")
        return None


def write_pinterest_landing(env: Environment, raw: dict) -> None:
    """Write pinterest_upload/<id>/index.html only (does not touch root wisdom.html)."""
    item_id = raw.get("id")
    if not item_id:
        raise ValueError("content entry missing id")

    template = env.get_template(PINTEREST_TEMPLATE)
    item = build_pinterest_item(raw)
    out_dir = os.path.join(PINTEREST_UPLOAD_ROOT, item_id)
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "index.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(template.render(item=item))


def generate_site():
    """
    Generate Pinterest landing pages under pinterest_upload/ and pin JPEGs under assets/images/pinterest/.
    Does not modify or overwrite root wisdom.html or emit wisdom_*.html in the project root.
    """
    env = Environment(loader=FileSystemLoader("."))

    with open(CONTENT_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    for post in data.get("general_posts", []):
        write_pinterest_landing(env, post)
        create_pinterest_pin(post["id"], post["title"], "Jerusalem Signet Wisdom")
        print(f"Generated Pinterest landing: {post['id']}")

    for tribe in data.get("tribes", []):
        write_pinterest_landing(env, tribe)
        tribe_title = tribe.get("english_name") or tribe.get("name") or tribe.get("id", "")
        create_pinterest_pin(tribe["id"], tribe_title, f"Tribe of {tribe_title}")
        print(f"Generated Pinterest landing: {tribe['id']}")


if __name__ == "__main__":
    generate_site()
