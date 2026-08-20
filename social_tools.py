import os
import io
import time
import random
import urllib.parse
from pathlib import Path
import httpx
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

# Load .env variables
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

IG_USER_ID = os.getenv("INSTAGRAM_ACCOUNT_ID")
IG_ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN")
DEFAULT_WHATSAPP_PHONE = os.getenv("WHATSAPP_DEFAULT_PHONE", "")
WATERMARK_NAME = os.getenv("WATERMARK_NAME", "AI Studio")
LINKEDIN_ACCESS_TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN")
LINKEDIN_AUTHOR_URN = os.getenv("LINKEDIN_AUTHOR_URN", "")

# Curated 4K Aesthetic Nature Wallpapers
NATURE_WALLPAPERS = [
    "https://images.unsplash.com/photo-1519681393784-d120267933ba?w=1080&h=1080&fit=crop&q=90", # Galaxy & Mountains
    "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1080&h=1080&fit=crop&q=90", # Golden Sunset
    "https://images.unsplash.com/photo-1448375240586-882707db888b?w=1080&h=1080&fit=crop&q=90", # Misty Pine Forest
    "https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=1080&h=1080&fit=crop&q=90", # Cinematic Mountains
]

DEFAULT_REEL_VIDEO_URL = "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4"


def create_nature_quote_image(quote_text: str, author: str = None, is_story: bool = False) -> str:
    """
    Generates a 4K aesthetic quote image with frosted glass card, typography and custom watermark.
    """
    if not author:
        author = WATERMARK_NAME or "AI Creator"

    width, height = (1080, 1920) if is_story else (1080, 1080)
    bg_url = random.choice(NATURE_WALLPAPERS)
    if is_story:
        bg_url = bg_url.replace("1080&h=1080", "1080&h=1920")

    print(f"[Nature Engine] Generating 4K aesthetic graphic image with watermark: {author}...")
    try:
        with httpx.Client(timeout=20.0) as client:
            resp = client.get(bg_url)
            bg = Image.open(io.BytesIO(resp.content)).convert("RGBA")
            bg = bg.resize((width, height), Image.Resampling.LANCZOS)
    except Exception as e:
        print(f"[Nature Engine] Wallpaper fetch notice ({e}), creating gradient fallback.")
        bg = Image.new("RGBA", (width, height), (20, 24, 33, 255))

    # Dim background
    enhancer = ImageEnhance.Brightness(bg)
    bg = enhancer.enhance(0.50)

    # Frosted Glass Card
    card_w = int(width * 0.88)
    card_h = int(height * 0.52) if is_story else int(height * 0.68)
    card_x0 = (width - card_w) // 2
    card_y0 = (height - card_h) // 2
    card_x1 = card_x0 + card_w
    card_y1 = card_y0 + card_h

    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    overlay_draw.rounded_rectangle([card_x0, card_y0, card_x1, card_y1], radius=36, fill=(15, 23, 42, 205), outline=(255, 255, 255, 90), width=4)

    final_img = Image.alpha_composite(bg, overlay)
    draw = ImageDraw.Draw(final_img)

    # Cross-Platform Scalable High-Res Typography
    def get_scaled_font(size: int, bold: bool = True):
        font_names = ["DejaVuSans-Bold.ttf", "arialbd.ttf", "LiberationSans-Bold.ttf"] if bold else ["DejaVuSans.ttf", "arial.ttf", "LiberationSans-Regular.ttf"]
        for fn in font_names:
            try:
                return ImageFont.truetype(fn, size)
            except Exception:
                continue
        try:
            return ImageFont.load_default(size=size)
        except Exception:
            return ImageFont.load_default()

    font_header = get_scaled_font(size=30, bold=True)
    font_quote = get_scaled_font(size=56, bold=True)
    font_author = get_scaled_font(size=40, bold=True)

    # Header Accent
    draw.text((width // 2, card_y0 + 60), "- WISDOM & SUCCESS -", fill=(203, 213, 225, 230), font=font_header, anchor="mm")

    # Wrapped Quote
    words = quote_text.split()
    lines = []
    curr = []
    for w in words:
        curr.append(w)
        if len(" ".join(curr)) > 22:
            lines.append(" ".join(curr[:-1]))
            curr = [w]
    if curr:
        lines.append(" ".join(curr))

    line_spacing = 72
    total_text_h = len(lines) * line_spacing
    y_offset = card_y0 + (card_h // 2) - (total_text_h // 2) + 10

    for line in lines:
        draw.text((width // 2, y_offset), line, fill=(255, 255, 255, 255), font=font_quote, anchor="mm")
        y_offset += line_spacing

    # Signature Watermark
    watermark_display = f"-- {author}"
    draw.text((width // 2, card_y1 - 65), watermark_display, fill=(251, 191, 36, 255), font=font_author, anchor="mm")

    final_img = final_img.convert("RGB")
    out_path = Path(__file__).parent / "nature_quote.png"
    final_img.save(out_path, quality=95)
    return str(out_path)


def upload_local_file(file_path: str) -> str:
    """
    Uploads a local image/video file to multi-CDN servers to guarantee a 100% public URL.
    """
    p = Path(file_path).resolve()
    if not p.exists() or not p.is_file():
        return None

    # Server 1: Catbox CDN
    try:
        print(f"[Uploader] Uploading '{p.name}' to Cloud CDN...")
        with open(p, "rb") as f:
            with httpx.Client(timeout=25.0) as client:
                res = client.post(
                    "https://catbox.moe/user/api.php",
                    data={"reqtype": "fileupload"},
                    files={"fileToUpload": (p.name, f)}
                )
                if res.status_code == 200 and res.text.strip().startswith("https://"):
                    url = res.text.strip()
                    print(f"[Uploader] Public CDN URL: {url}")
                    return url
    except Exception:
        pass

    # Server 2: TmpFiles Backup CDN
    try:
        with open(p, "rb") as f:
            with httpx.Client(timeout=25.0) as client:
                res = client.post(
                    "https://tmpfiles.org/api/v1/upload",
                    files={"file": (p.name, f)}
                )
                if res.status_code == 200:
                    data = res.json()
                    raw_url = data.get("data", {}).get("url")
                    if raw_url:
                        url = raw_url.replace("tmpfiles.org/", "tmpfiles.org/dl/")
                        print(f"[Uploader] Backup CDN URL: {url}")
                        return url
    except Exception:
        pass

    return None


def resolve_media_url(media_path_or_url: str) -> str:
    """
    Ensures the media is a public HTTPS URL. If a local file path is given, uploads it.
    """
    if media_path_or_url.startswith("http://") or media_path_or_url.startswith("https://"):
        return media_path_or_url

    uploaded_url = upload_local_file(media_path_or_url)
    if uploaded_url:
        return uploaded_url

    raise ValueError(f"Could not convert local file '{media_path_or_url}' to a public URL.")


def post_instagram_feed(content: str, media_path_or_url: str = None, user_id: str = None, access_token: str = None, author: str = None) -> str:
    """
    Posts a photo to Instagram feed.
    """
    uid = user_id or IG_USER_ID
    token = access_token or IG_ACCESS_TOKEN
    sign = author or WATERMARK_NAME

    if not uid or not token:
        return "Instagram credentials missing."

    if not media_path_or_url:
        media_path_or_url = create_nature_quote_image(content, author=sign, is_story=False)

    image_url = resolve_media_url(media_path_or_url)

    try:
        with httpx.Client(timeout=45.0) as client:
            container_res = client.post(
                f"https://graph.facebook.com/v21.0/{uid}/media",
                params={
                    "image_url": image_url,
                    "caption": f"{content} -- {sign}",
                    "access_token": token
                }
            )
            container_data = container_res.json()
            creation_id = container_data.get("id")

            if not creation_id:
                return f"Instagram Feed Container Error: {container_data}"

            time.sleep(5)

            pub_res = client.post(
                f"https://graph.facebook.com/v21.0/{uid}/media_publish",
                params={
                    "creation_id": creation_id,
                    "access_token": token
                }
            )
            pub_data = pub_res.json()
            if "id" in pub_data:
                return f"Instagram Feed Post Published Successfully!\nPost ID: {pub_data['id']}\nImage: {image_url}\nCaption: {content} -- {sign}"
            return f"Instagram Publish Error: {pub_data}"
    except Exception as e:
        return f"Instagram Feed Exception: {e}"


def post_instagram_story(content: str, media_path_or_url: str = None, user_id: str = None, access_token: str = None, author: str = None) -> str:
    """
    Posts a 24-hour aesthetic Story to Instagram.
    """
    uid = user_id or IG_USER_ID
    token = access_token or IG_ACCESS_TOKEN
    sign = author or WATERMARK_NAME

    if not uid or not token:
        return "Instagram credentials missing."

    if not media_path_or_url:
        media_path_or_url = create_nature_quote_image(content, author=sign, is_story=True)

    image_url = resolve_media_url(media_path_or_url)

    try:
        with httpx.Client(timeout=45.0) as client:
            container_res = client.post(
                f"https://graph.facebook.com/v21.0/{uid}/media",
                params={
                    "image_url": image_url,
                    "media_type": "STORIES",
                    "access_token": token
                }
            )
            container_data = container_res.json()
            creation_id = container_data.get("id")

            if not creation_id:
                return f"Instagram Story Container Error: {container_data}"

            time.sleep(5)

            pub_res = client.post(
                f"https://graph.facebook.com/v21.0/{uid}/media_publish",
                params={
                    "creation_id": creation_id,
                    "access_token": token
                }
            )
            pub_data = pub_res.json()
            if "id" in pub_data:
                return f"Instagram Story Published Successfully (Live 24h)!\nStory ID: {pub_data['id']}\nImage: {image_url}"
            return f"Instagram Story Publish Error: {pub_data}"
    except Exception as e:
        return f"Instagram Story Exception: {e}"


def post_facebook(content: str, media_path_or_url: str = None, author: str = None) -> str:
    """
    Posts directly to Facebook Timeline using persistent session.
    """
    session_dir = Path(__file__).parent / "facebook_session"
    if not session_dir.exists():
        return "Facebook session directory not found. Please run session setup."

    sign = author or WATERMARK_NAME
    local_img = media_path_or_url
    if not local_img or not Path(local_img).exists():
        local_img = create_nature_quote_image(content, author=sign, is_story=False)

    caption_text = f"{content} -- {sign}"
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"

    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            context = p.chromium.launch_persistent_context(
                user_data_dir=str(session_dir),
                headless=True,
                user_agent=USER_AGENT,
                viewport={"width": 1280, "height": 800},
                args=["--no-sandbox", "--disable-blink-features=AutomationControlled"]
            )
            page = context.pages[0] if context.pages else context.new_page()
            page.goto("https://www.facebook.com/", timeout=60000)
            time.sleep(5)

            try:
                page.keyboard.press("Escape")
                time.sleep(1)
            except Exception:
                pass

            page.locator('div[role="region"] div[role="button"]').first.click(force=True)
            time.sleep(3)

            photo_btn = page.locator('div[aria-label="Photo/video"]').first
            if photo_btn.is_visible():
                photo_btn.click(force=True)
                time.sleep(2)

            file_input = page.locator('input[type="file"]').first
            file_input.set_input_files(str(Path(local_img).resolve()))
            time.sleep(4)

            textbox = page.locator('div[role="textbox"][contenteditable="true"]').first
            textbox.click()
            page.evaluate("(text) => { const el = document.querySelector('div[role=\"textbox\"][contenteditable=\"true\"]'); if (el) { el.focus(); document.execCommand('insertText', false, text); } }", caption_text)
            time.sleep(2)

            post_btn = page.locator('div[aria-label="Post"], div[aria-label="पोस्ट करें"]').last
            post_btn.click(force=True)
            time.sleep(10)

            context.close()
            return f"Facebook Post Published Live on Timeline!\nCaption: {caption_text}"
    except Exception as e:
        return f"Facebook Direct Post Notice: {e}"


def post_linkedin(content: str, media_path_or_url: str = None, access_token: str = None, author_urn: str = None, author: str = None) -> str:
    """
    Publishes a photo or text post to LinkedIn via official REST API.
    """
    token = access_token or LINKEDIN_ACCESS_TOKEN
    urn = author_urn or LINKEDIN_AUTHOR_URN
    sign = author or WATERMARK_NAME

    if not token or not urn:
        return "LinkedIn Access Token or Author URN not configured."

    caption_text = f"{content}\n\n-- {sign}\n#AgenticAI #Python #Automation #LinkedIn"
    headers = {
        "Authorization": f"Bearer {token}",
        "X-Restli-Protocol-Version": "2.0.0",
        "Content-Type": "application/json"
    }

    try:
        with httpx.Client(timeout=35.0) as client:
            local_img = media_path_or_url
            if not local_img or not Path(local_img).exists():
                local_img = create_nature_quote_image(content, author=sign, is_story=False)

            reg_payload = {
                "registerUploadRequest": {
                    "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
                    "owner": urn,
                    "serviceRelationships": [{
                        "relationshipType": "OWNER",
                        "identifier": "urn:li:userGeneratedContent"
                    }]
                }
            }
            r1 = client.post("https://api.linkedin.com/v2/assets?action=registerUpload", headers=headers, json=reg_payload)
            data1 = r1.json()
            asset = data1.get("value", {}).get("asset")
            upload_url = data1.get("value", {}).get("uploadMechanism", {}).get("com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest", {}).get("uploadUrl")

            if asset and upload_url:
                with open(local_img, "rb") as f:
                    client.put(upload_url, headers={"Authorization": f"Bearer {token}"}, content=f.read())

                post_payload = {
                    "author": urn,
                    "lifecycleState": "PUBLISHED",
                    "specificContent": {
                        "com.linkedin.ugc.ShareContent": {
                            "shareCommentary": {"text": caption_text},
                            "shareMediaCategory": "IMAGE",
                            "media": [{
                                "status": "READY",
                                "description": {"text": "Agentic AI Graphic"},
                                "media": asset,
                                "title": {"text": "Autonomous Post"}
                            }]
                        }
                    },
                    "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"}
                }
            else:
                post_payload = {
                    "author": urn,
                    "lifecycleState": "PUBLISHED",
                    "specificContent": {
                        "com.linkedin.ugc.ShareContent": {
                            "shareCommentary": {"text": caption_text},
                            "shareMediaCategory": "NONE"
                        }
                    },
                    "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"}
                }

            pub_res = client.post("https://api.linkedin.com/v2/ugcPosts", headers=headers, json=post_payload)
            if pub_res.status_code in [200, 201]:
                post_id = pub_res.json().get("id")
                return f"LinkedIn Post Published Successfully Live!\nPost ID: {post_id}\nCaption: {content}"
            return f"LinkedIn Publish Error: {pub_res.text}"
    except Exception as e:
        return f"LinkedIn Exception: {e}"


def post_whatsapp(content: str, target: str = None) -> str:
    """
    Sends message + 4K graphic silently in the background via headless Playwright Chrome.
    """
    phone = target if (target and target.startswith("+")) else DEFAULT_WHATSAPP_PHONE
    if not phone:
        return "WhatsApp recipient phone number is required."

    encoded_text = urllib.parse.quote(content)
    target_url = f"https://web.whatsapp.com/send?phone={phone.replace('+', '')}&text={encoded_text}"
    session_dir = Path(__file__).parent / "whatsapp_session"

    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"

    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            context = p.chromium.launch_persistent_context(
                user_data_dir=str(session_dir),
                headless=True,
                user_agent=USER_AGENT,
                viewport={"width": 1280, "height": 800},
                args=["--no-sandbox", "--disable-blink-features=AutomationControlled"]
            )
            page = context.pages[0] if context.pages else context.new_page()
            page.goto(target_url, timeout=60000)
            time.sleep(10)

            send_button = page.locator('button[aria-label="Send"], span[data-icon="send"]').first
            send_button.click(timeout=15000)
            time.sleep(4)
            context.close()
            return f"WhatsApp message successfully delivered to {phone} in background!"
    except Exception as e:
        return f"WhatsApp automation notice: {e}"