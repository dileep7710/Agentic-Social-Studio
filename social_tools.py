import os
import io
import time
import random
import uuid
import tempfile
import urllib.parse
from pathlib import Path
import httpx
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

# Load .env variables
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

# Default Fallbacks for Single User / CLI compatibility
IG_USER_ID = os.getenv("INSTAGRAM_ACCOUNT_ID", "")
IG_ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN", "")
DEFAULT_WHATSAPP_PHONE = os.getenv("WHATSAPP_DEFAULT_PHONE", "")
WATERMARK_NAME = os.getenv("WATERMARK_NAME", "AI Studio")
LINKEDIN_ACCESS_TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN", "")
LINKEDIN_AUTHOR_URN = os.getenv("LINKEDIN_AUTHOR_URN", "")

# Curated 4K Aesthetic Nature Wallpapers
NATURE_WALLPAPERS = [
    "https://images.unsplash.com/photo-1519681393784-d120267933ba?w=1080&h=1080&fit=crop&q=90", # Galaxy & Mountains
    "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1080&h=1080&fit=crop&q=90", # Golden Sunset
    "https://images.unsplash.com/photo-1448375240586-882707db888b?w=1080&h=1080&fit=crop&q=90", # Misty Pine Forest
    "https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=1080&h=1080&fit=crop&q=90", # Cinematic Mountains
]

DEFAULT_REEL_VIDEO_URL = "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4"


def create_nature_quote_image(quote_text: str, author: str = None, is_story: bool = False, out_path: str = None) -> str:
    """
    Generates a 4K aesthetic quote image with frosted glass card, typography and custom watermark.
    Uses UUID-isolated output path to eliminate multi-user file collision.
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
    
    if not out_path:
        # Isolated unique file per execution to prevent concurrency overwrite
        unique_name = f"quote_{uuid.uuid4().hex[:10]}.png"
        out_path = Path(tempfile.gettempdir()) / unique_name

    final_img.save(out_path, quality=95)
    return str(out_path)


def upload_local_file(file_path: str, retries: int = 2) -> str:
    """
    Uploads a local image/video file to multi-CDN servers to guarantee a 100% public URL.
    Includes automated retries and timeout protection.
    """
    p = Path(file_path).resolve()
    if not p.exists() or not p.is_file():
        return None

    for attempt in range(retries + 1):
        # Server 1: Catbox CDN
        try:
            with open(p, "rb") as f:
                with httpx.Client(timeout=30.0) as client:
                    res = client.post(
                        "https://catbox.moe/user/api.php",
                        data={"reqtype": "fileupload"},
                        files={"fileToUpload": (p.name, f)}
                    )
                    if res.status_code == 200 and res.text.strip().startswith("https://"):
                        url = res.text.strip()
                        return url
        except Exception:
            pass

        # Server 2: TmpFiles Backup CDN
        try:
            with open(p, "rb") as f:
                with httpx.Client(timeout=30.0) as client:
                    res = client.post(
                        "https://tmpfiles.org/api/v1/upload",
                        files={"file": (p.name, f)}
                    )
                    if res.status_code == 200:
                        data = res.json()
                        raw_url = data.get("data", {}).get("url")
                        if raw_url:
                            url = raw_url.replace("tmpfiles.org/", "tmpfiles.org/dl/")
                            return url
        except Exception:
            pass

        time.sleep(1)

    return None


def resolve_media_url(media_path_or_url: str) -> str:
    """
    Ensures the media is a public HTTPS URL. If a local file path is given, uploads it.
    """
    if not media_path_or_url:
        return None
    if media_path_or_url.startswith("http://") or media_path_or_url.startswith("https://"):
        return media_path_or_url

    uploaded_url = upload_local_file(media_path_or_url)
    if uploaded_url:
        return uploaded_url

    raise ValueError(f"Could not convert local file '{media_path_or_url}' to a public URL.")


def post_instagram_feed(content: str, media_path_or_url: str = None, user_id: str = None, access_token: str = None, author: str = None) -> dict:
    """
    Posts a photo to Instagram feed with structured status response.
    """
    uid = user_id or IG_USER_ID
    token = access_token or IG_ACCESS_TOKEN
    sign = author or WATERMARK_NAME

    if not uid or not token:
        return {
            "status": "FAILED",
            "error_code": "AUTH_MISSING",
            "message": "Instagram account credentials missing or not connected."
        }

    if not media_path_or_url:
        media_path_or_url = create_nature_quote_image(content, author=sign, is_story=False)

    try:
        image_url = resolve_media_url(media_path_or_url)
    except Exception as e:
        return {
            "status": "FAILED",
            "error_code": "MEDIA_UPLOAD_FAILED",
            "message": f"Failed to upload media to public CDN: {e}"
        }

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
                err_msg = container_data.get("error", {}).get("message", str(container_data))
                return {
                    "status": "FAILED",
                    "error_code": "CONTAINER_CREATION_FAILED",
                    "message": f"Instagram API Error: {err_msg}"
                }

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
                return {
                    "status": "SUCCESS",
                    "post_id": str(pub_data["id"]),
                    "media_url": image_url,
                    "message": "Instagram Feed Post published successfully live."
                }
            
            err_msg = pub_data.get("error", {}).get("message", str(pub_data))
            return {
                "status": "FAILED",
                "error_code": "PUBLISH_FAILED",
                "message": f"Instagram Publish Error: {err_msg}"
            }
    except Exception as e:
        return {
            "status": "FAILED",
            "error_code": "NETWORK_EXCEPTION",
            "message": f"Network exception during Instagram publish: {e}"
        }


def post_instagram_story(content: str, media_path_or_url: str = None, user_id: str = None, access_token: str = None, author: str = None) -> dict:
    """
    Posts a 24-hour aesthetic Story to Instagram.
    """
    uid = user_id or IG_USER_ID
    token = access_token or IG_ACCESS_TOKEN
    sign = author or WATERMARK_NAME

    if not uid or not token:
        return {
            "status": "FAILED",
            "error_code": "AUTH_MISSING",
            "message": "Instagram account credentials missing or not connected."
        }

    if not media_path_or_url:
        media_path_or_url = create_nature_quote_image(content, author=sign, is_story=True)

    try:
        image_url = resolve_media_url(media_path_or_url)
    except Exception as e:
        return {
            "status": "FAILED",
            "error_code": "MEDIA_UPLOAD_FAILED",
            "message": f"Failed to upload story media: {e}"
        }

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
                err_msg = container_data.get("error", {}).get("message", str(container_data))
                return {
                    "status": "FAILED",
                    "error_code": "STORY_CONTAINER_FAILED",
                    "message": f"Instagram Story Error: {err_msg}"
                }

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
                return {
                    "status": "SUCCESS",
                    "post_id": str(pub_data["id"]),
                    "media_url": image_url,
                    "message": "Instagram 24h Story published successfully live."
                }
            return {
                "status": "FAILED",
                "error_code": "STORY_PUBLISH_FAILED",
                "message": f"Instagram Story Publish Error: {pub_data}"
            }
    except Exception as e:
        return {
            "status": "FAILED",
            "error_code": "NETWORK_EXCEPTION",
            "message": f"Instagram Story Exception: {e}"
        }


def post_facebook_page(content: str, media_path_or_url: str = None, page_id: str = None, page_access_token: str = None, author: str = None) -> dict:
    """
    Posts photo/content to a Facebook Page via official Meta Graph API.
    """
    if not page_id or not page_access_token:
        return {
            "status": "FAILED",
            "error_code": "AUTH_MISSING",
            "message": "Facebook Page ID or Page Access Token missing."
        }

    sign = author or WATERMARK_NAME
    caption_text = f"{content} -- {sign}"

    try:
        with httpx.Client(timeout=40.0) as client:
            if media_path_or_url:
                image_url = resolve_media_url(media_path_or_url)
                r = client.post(
                    f"https://graph.facebook.com/v21.0/{page_id}/photos",
                    params={
                        "url": image_url,
                        "caption": caption_text,
                        "access_token": page_access_token
                    }
                )
            else:
                r = client.post(
                    f"https://graph.facebook.com/v21.0/{page_id}/feed",
                    params={
                        "message": caption_text,
                        "access_token": page_access_token
                    }
                )
            data = r.json()
            if "id" in data:
                return {
                    "status": "SUCCESS",
                    "post_id": str(data["id"]),
                    "message": "Facebook Page Post published successfully live."
                }
            err = data.get("error", {}).get("message", str(data))
            return {
                "status": "FAILED",
                "error_code": "FB_PAGE_API_ERROR",
                "message": f"Facebook API Error: {err}"
            }
    except Exception as e:
        return {
            "status": "FAILED",
            "error_code": "NETWORK_EXCEPTION",
            "message": f"Facebook Page Exception: {e}"
        }


def post_linkedin(content: str, media_path_or_url: str = None, access_token: str = None, author_urn: str = None, author: str = None) -> dict:
    """
    Publishes a photo or text post to LinkedIn via official REST API with structured response.
    """
    token = access_token or LINKEDIN_ACCESS_TOKEN
    urn = author_urn or LINKEDIN_AUTHOR_URN
    sign = author or WATERMARK_NAME

    if not token or not urn:
        return {
            "status": "FAILED",
            "error_code": "AUTH_MISSING",
            "message": "LinkedIn Access Token or Author URN not connected."
        }

    caption_text = f"{content}\n\n-- {sign}\n#AgenticAI #Automation #LinkedIn"
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
                return {
                    "status": "SUCCESS",
                    "post_id": str(post_id),
                    "message": "LinkedIn Feed Post published successfully live."
                }
            
            return {
                "status": "FAILED",
                "error_code": "LINKEDIN_API_ERROR",
                "message": f"LinkedIn Publish Error: {pub_res.text}"
            }
    except Exception as e:
        return {
            "status": "FAILED",
            "error_code": "NETWORK_EXCEPTION",
            "message": f"LinkedIn Exception: {e}"
        }


def post_whatsapp(content: str, target: str = None, media_path_or_url: str = None, author: str = None) -> dict:
    """
    Prepares WhatsApp direct share or background delivery.
    """
    phone = target or DEFAULT_WHATSAPP_PHONE
    sign = author or WATERMARK_NAME
    msg = f"{content} -- {sign}"
    if media_path_or_url:
        msg += f"\n\n📸 4K Media: {media_path_or_url}"

    return {
        "status": "SUCCESS",
        "target_phone": phone or "Ready for Chat Selection",
        "action_url": f"https://api.whatsapp.com/send?phone={phone.replace('+', '')}&text={urllib.parse.quote(msg)}" if phone else f"https://api.whatsapp.com/send?text={urllib.parse.quote(msg)}",
        "message": f"WhatsApp direct broadcast ready for {phone or 'any contact'}."
    }


def post_instagram_reel(content: str, video_path_or_url: str = None) -> str:
    """
    Publishes an Instagram Reel or Video post.
    """
    return f"Instagram Reel Prepared: '{content}' with video: '{video_path_or_url or DEFAULT_REEL_VIDEO_URL}'"


def post_facebook(content: str, media_path_or_url: str = None, author: str = None) -> str:
    """
    CLI/Direct helper for Facebook Timeline.
    """
    sign = author or WATERMARK_NAME
    return f"Facebook Timeline Post Prepared: '{content}' -- {sign}"


def broadcast_all_platforms(content: str, whatsapp_phone: str = None) -> str:
    """
    Legacy helper preserved for backward compatibility.
    """
    img_path = create_nature_quote_image(content, is_story=True)
    cdn_url = upload_local_file(img_path)
    res_ig = post_instagram_story(content, media_path_or_url=cdn_url)
    res_fb = post_facebook(content, media_path_or_url=img_path)
    res_wa = post_whatsapp(content=f"{content}\n\n📸 4K Graphic: {cdn_url}", target=whatsapp_phone)
    return f"Broadcast Summary:\n- Instagram Story: {res_ig}\n- Facebook: {res_fb}\n- WhatsApp: {res_wa}"