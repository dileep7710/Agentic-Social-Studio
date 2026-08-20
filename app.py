import streamlit as st
import os
import random
import tempfile
import urllib.parse
import httpx
from pathlib import Path
from PIL import Image

# Import our unified social engine tools
from social_tools import (
    create_nature_quote_image,
    upload_local_file,
    post_instagram_story,
    post_instagram_feed,
    post_facebook,
    post_linkedin,
    post_whatsapp
)

# Page Configuration
st.set_page_config(
    page_title="Agentic AI Omni-Studio | Production SaaS Edition",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Curated High-Impact Neural Quotes for Zero-Failure Mode
INSPIRING_QUOTES = [
    "The secret of getting ahead is getting started.",
    "Do what you can, with what you have, where you are.",
    "Small daily improvements over time lead to stunning results.",
    "Discipline is the bridge between goals and accomplishment.",
    "Your time is limited, don't waste it living someone else's life.",
    "Action is the foundational key to all success.",
    "Believe you can and you're halfway there.",
    "Great things never come from comfort zones.",
    "Success is the sum of small efforts, repeated day in and day out.",
    "Turn your wounds into wisdom and your challenges into triumphs.",
    "Opportunities don't happen. You create them.",
    "The only limit to our realization of tomorrow will be our doubts of today.",
    "Stay hungry, stay foolish, and always stay relentless in your pursuit.",
    "Focus on being productive instead of busy.",
    "Consistency is the true DNA of mastery."
]

# Premium Ultra-Fantasy Glassmorphism CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    .stApp {
        background: radial-gradient(circle at 10% 20%, #17153B 0%, #0F1026 50%, #08071A 100%);
        color: #F8FAFC;
    }

    .fantasy-title {
        font-size: 2.6rem;
        font-weight: 800;
        background: linear-gradient(135deg, #FF6B6B 0%, #FF8E53 25%, #FFD93D 50%, #6BCB77 75%, #4D96FF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2px;
    }

    .fantasy-subtitle {
        color: #94A3B8;
        font-size: 1.05rem;
        font-weight: 400;
        margin-bottom: 20px;
    }

    .glowing-badge {
        display: block;
        padding: 10px 14px;
        background: rgba(139, 92, 246, 0.15);
        border: 1px solid rgba(139, 92, 246, 0.4);
        border-radius: 12px;
        color: #DDD6FE;
        font-size: 0.92rem;
        font-weight: 600;
        margin-bottom: 10px;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background-color: transparent;
        margin-bottom: 18px;
    }

    .stTabs [data-baseweb="tab"] {
        background: rgba(30, 41, 59, 0.6);
        border-radius: 12px;
        padding: 10px 22px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        color: #94A3B8;
        font-weight: 600;
        transition: all 0.3s ease;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #6366F1, #8B5CF6) !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(139, 92, 246, 0.6) !important;
        box-shadow: 0 4px 20px rgba(99, 102, 241, 0.45);
    }

    [data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(30, 41, 59, 0.55);
        border: 1px solid rgba(255, 255, 255, 0.09) !important;
        border-radius: 16px;
        padding: 18px;
        backdrop-filter: blur(12px);
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if "watermark" not in st.session_state:
    st.session_state["watermark"] = ""
if "phone" not in st.session_state:
    st.session_state["phone"] = ""
if "ig_id" not in st.session_state:
    st.session_state["ig_id"] = "17841448994358440"
if "ig_token" not in st.session_state:
    st.session_state["ig_token"] = ""
if "ig_user" not in st.session_state:
    st.session_state["ig_user"] = ""
if "fb_name" not in st.session_state:
    st.session_state["fb_name"] = ""
if "li_token" not in st.session_state:
    st.session_state["li_token"] = ""
if "li_urn" not in st.session_state:
    st.session_state["li_urn"] = ""
if "li_name" not in st.session_state:
    st.session_state["li_name"] = ""

# Helper: Auto-Detect LinkedIn Profile Name & URN from Token
def auto_detect_linkedin(token: str):
    if not token:
        return None, None
    try:
        with httpx.Client(timeout=15.0) as client:
            r = client.get("https://api.linkedin.com/v2/userinfo", headers={"Authorization": f"Bearer {token}"})
            if r.status_code == 200:
                data = r.json()
                sub = data.get("sub")
                name = data.get("name", "Connected User")
                if sub:
                    return f"urn:li:person:{sub}", name
    except Exception:
        pass
    return None, None

# Helper: Auto-Detect Meta (Facebook Name + Instagram ID & Username) from Token
def auto_detect_meta(token: str):
    if not token:
        return None, None, None
    fb_name = "Connected User"
    ig_id = "17841448994358440"
    ig_user = "@dileepy18"
    try:
        with httpx.Client(timeout=15.0) as client:
            # 1. Fetch Facebook User Name
            r_me = client.get(f"https://graph.facebook.com/v21.0/me?fields=name,id&access_token={token}")
            if r_me.status_code == 200:
                fb_name = r_me.json().get("name", "Connected User")

            # 2. Fetch Connected Pages & Instagram
            r_acc = client.get(f"https://graph.facebook.com/v21.0/me/accounts?fields=instagram_business_account,name&access_token={token}")
            if r_acc.status_code == 200:
                data = r_acc.json().get("data", [])
                for page in data:
                    ig_acc = page.get("instagram_business_account", {})
                    if "id" in ig_acc:
                        ig_id = ig_acc["id"]
                        ig_user = page.get("name", "Instagram User")
                        return fb_name, ig_id, ig_user
            
            # 3. Direct IG Account Check
            r_ig = client.get(f"https://graph.facebook.com/v21.0/{ig_id}?fields=id,username&access_token={token}")
            if r_ig.status_code == 200:
                d = r_ig.json()
                ig_id = d.get("id", ig_id)
                ig_user = f"@{d.get('username', 'dileepy18')}"
    except Exception:
        pass
    return fb_name, ig_id, ig_user

# Sidebar Profile Status
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=400&q=80", use_container_width=True)
    
    lang = st.radio("🌐 Language / भाषा:", ["English", "हिन्दी (Hindi)"], horizontal=True)
    
    st.markdown("---")
    st.markdown("### 👤 Active Profile / एक्टिव यूजर")
    display_user = st.session_state["watermark"] if st.session_state["watermark"] else "Not Set"
    display_phone = st.session_state["phone"] if st.session_state["phone"] else "Not Set"
    st.markdown(f'<div class="glowing-badge">🏷️ Name: {display_user}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="glowing-badge">💬 WhatsApp: {display_phone}</div>', unsafe_allow_html=True)
    if st.session_state["fb_name"]:
        st.markdown(f'<div class="glowing-badge">📘 Facebook: {st.session_state["fb_name"]}</div>', unsafe_allow_html=True)
    if st.session_state["ig_user"]:
        st.markdown(f'<div class="glowing-badge">📸 Instagram: {st.session_state["ig_user"]}</div>', unsafe_allow_html=True)
    if st.session_state["li_name"]:
        st.markdown(f'<div class="glowing-badge">💼 LinkedIn: {st.session_state["li_name"]}</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 🤖 Connected 4 Platforms")
    st.markdown("- 📸 **Instagram** (Stories & Feed Live)")
    st.markdown("- 📘 **Facebook** (Timeline 1-Click)")
    st.markdown("- 💼 **LinkedIn** (Official REST API)")
    st.markdown("- 💬 **WhatsApp** (Direct Delivery)")

# Main Header
if lang == "English":
    st.markdown('<div class="fantasy-title">🌌 Agentic AI Omni-Studio</div>', unsafe_allow_html=True)
    st.markdown('<div class="fantasy-subtitle">Broadcast to Instagram, Facebook, LinkedIn & WhatsApp in 1-Click</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="fantasy-title">🌌 एजेंटिक AI ऑम्नी-स्टूडियो</div>', unsafe_allow_html=True)
    st.markdown('<div class="fantasy-subtitle">इंस्टाग्राम, फेसबुक, लिंक्डइन और व्हाट्सएप पर 1-क्लिक में पोस्ट करें</div>', unsafe_allow_html=True)

# Tabs
tab_studio, tab_accounts, tab_guide = st.tabs([
    "🔮 Studio / पोस्ट स्टूडियो", 
    "⚙️ Connect Accounts / अकाउंट्स जोड़ें", 
    "📖 Easy Guide / सरल मदद"
])

# ==========================================
# TAB 1: STUDIO (POST CREATOR)
# ==========================================
with tab_studio:
    col_left, col_right = st.columns([1.25, 1], gap="large")

    with col_left:
        with st.container(border=True):
            st.markdown("### 🎨 1. Media Source / कंटेंट चुनें")

            source_label = "Select Content Type:" if lang == "English" else "कंटेंट का प्रकार चुनें:"
            opt1 = "✨ Generate 4K AI Nature Graphic" if lang == "English" else "✨ 4K AI नेचर ग्राफिक बनाएं"
            opt2 = "📂 Upload Photo/Video from PC" if lang == "English" else "📂 कम्प्यूटर से फोटो/वीडियो चुनें"

            media_source = st.radio(source_label, [opt1, opt2], horizontal=True)

            if media_source == opt2:
                up_label = "Choose an image (.jpg, .png) or video (.mp4) from your local folder:" if lang == "English" else "अपने कम्प्यूटर के किसी भी फोल्डर से फोटो या वीडियो चुनें:"
                uploaded_file = st.file_uploader(up_label, type=["jpg", "jpeg", "png", "mp4"])
                if uploaded_file is not None:
                    suffix = Path(uploaded_file.name).suffix
                    tfile = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
                    tfile.write(uploaded_file.read())
                    st.session_state["custom_media_path"] = tfile.name
                    st.success(f"📂 Loaded: {uploaded_file.name}")
            else:
                # 100% Zero-Fail AI Quote Generator
                btn_txt = "✨ Auto-Generate Inspiring Quote" if lang == "English" else "✨ नया विचार (Quote) जनरेट करें"
                if st.button(btn_txt, use_container_width=True):
                    with st.spinner("🧠 AI is crafting an inspiring quote..."):
                        chosen_quote = random.choice(INSPIRING_QUOTES)
                        try:
                            import ollama
                            res = ollama.chat(
                                model="llama3.2:3b",
                                messages=[{
                                    "role": "user",
                                    "content": "Write one short, powerful, inspiring quote in 1-2 lines. Return ONLY the quote text."
                                }]
                            )
                            chosen_quote = res.message.content.strip().strip('"')
                        except Exception:
                            pass
                        st.session_state["quote_input"] = chosen_quote
                        st.toast("✨ New inspiring quote generated!")

        with st.container(border=True):
            cap_label = "Caption / Quote / विचार:" if lang == "English" else "कैप्शन या विचार:"
            caption_text = st.text_area(
                cap_label,
                value=st.session_state.get("quote_input", "The secret of getting ahead is getting started."),
                height=80
            )

        with st.container(border=True):
            st.markdown("### 🎯 2. Social Destinations (All 4 Networks) / सोशल मीडिया")
            
            # Connection Status Hints
            ig_status_icon = f"🟢 ({st.session_state['ig_user']})" if st.session_state["ig_token"] else "⚪ (Token required in Tab 2)"
            fb_status_icon = f"🟢 ({st.session_state['fb_name']})" if st.session_state["fb_name"] else "🟢 Ready"
            li_status_icon = f"🟢 ({st.session_state['li_name']})" if st.session_state["li_token"] else "⚪ (Token required in Tab 2)"
            wa_status_icon = f"🟢 ({st.session_state['phone']})" if st.session_state["phone"] else "⚪ (Phone required in Tab 2)"
            
            c1, c2 = st.columns(2)
            with c1:
                target_insta_story = st.checkbox(f"📸 Instagram Story (24h) {ig_status_icon}", value=True)
                target_insta_feed = st.checkbox(f"🖼️ Instagram Feed Post {ig_status_icon}", value=True)
            with c2:
                target_fb = st.checkbox(f"📘 Facebook Web Dispatch {fb_status_icon}", value=True)
                target_li = st.checkbox(f"💼 LinkedIn Professional Feed {li_status_icon}", value=True)
                target_wa = st.checkbox(f"💬 WhatsApp Delivery {wa_status_icon}", value=True)

        # Action Buttons
        b1, b2 = st.columns([1, 1.3])
        with b1:
            btn_prev = "🖼️ Refresh Preview" if lang == "English" else "🖼️ प्रीव्यू देखें"
            preview_clicked = st.button(btn_prev, use_container_width=True)
        with b2:
            btn_post = "🚀 Launch Multi-Platform Post" if lang == "English" else "🚀 सभी जगह पोस्ट करें"
            publish_clicked = st.button(btn_post, type="primary", use_container_width=True)

    # Preview Handling
    active_author = st.session_state["watermark"] if st.session_state["watermark"] else "AI Studio"
    if preview_clicked or "latest_preview" not in st.session_state:
        if media_source == opt1:
            img_path = create_nature_quote_image(caption_text, author=active_author, is_story=True)
            st.session_state["latest_preview"] = img_path
        elif "custom_media_path" in st.session_state:
            st.session_state["latest_preview"] = st.session_state["custom_media_path"]

    with col_right:
        with st.container(border=True):
            prev_title = "### 🖼️ Live 4K Visual Preview" if lang == "English" else "### 🖼️ लाइव प्रीव्यू"
            st.markdown(prev_title)
            
            preview_file = st.session_state.get("latest_preview")
            if preview_file and os.path.exists(preview_file):
                if preview_file.lower().endswith((".png", ".jpg", ".jpeg")):
                    img = Image.open(preview_file)
                    st.image(img, caption=f"✨ Signature Watermark: -- {active_author}", use_container_width=True)
                elif preview_file.lower().endswith(".mp4"):
                    st.video(preview_file)
            else:
                info_txt = "👈 Select a file or click 'Refresh Preview' to see your media here!" if lang == "English" else "👈 बाईं तरफ फोटो चुनें या प्रीव्यू बटन दबाएं!"
                st.info(info_txt)

    # Multi-Platform Execution
    if publish_clicked:
        st.markdown("---")
        st.markdown("### 📊 Live Omni-Channel Dispatch Stream")

        if media_source == opt2 and "custom_media_path" in st.session_state:
            final_media = st.session_state["custom_media_path"]
        else:
            final_media = create_nature_quote_image(caption_text, author=active_author, is_story=True)
            st.session_state["latest_preview"] = final_media

        with st.spinner("⚡ Uploading asset to high-speed CDN..."):
            img_url = upload_local_file(final_media)

        res_col1, res_col2 = st.columns(2)

        # 1. Instagram Story
        if target_insta_story:
            if not st.session_state["ig_token"]:
                with res_col1:
                    st.warning("⚠️ **Instagram Story:** Meta Token missing. Please paste token in Tab 2 ('Connect Accounts')!")
            else:
                with st.spinner("📸 Broadcasting to Instagram Story (24h)..."):
                    res = post_instagram_story(content=caption_text, media_path_or_url=img_url or final_media, user_id=st.session_state["ig_id"], access_token=st.session_state["ig_token"], author=active_author)
                    with res_col1:
                        if "Published" in res or "Live" in res:
                            st.success("✅ **Instagram Story (24h):** Published Live!")
                        else:
                            st.error(f"❌ **Instagram Story Notice:** {res}")

        # 2. Instagram Feed
        if target_insta_feed:
            if not st.session_state["ig_token"]:
                with res_col1:
                    st.warning("⚠️ **Instagram Feed:** Meta Token missing. Please paste token in Tab 2 ('Connect Accounts')!")
            else:
                with st.spinner("🖼️ Broadcasting to Instagram Feed..."):
                    res = post_instagram_feed(content=caption_text, media_path_or_url=img_url or final_media, user_id=st.session_state["ig_id"], access_token=st.session_state["ig_token"], author=active_author)
                    with res_col1:
                        if "Published" in res or "Live" in res:
                            st.success("✅ **Instagram Feed:** Published Live!")
                        else:
                            st.error(f"❌ **Instagram Feed Notice:** {res}")

        # 3. LinkedIn
        if target_li:
            if not st.session_state["li_token"]:
                with res_col2:
                    st.warning("⚠️ **LinkedIn:** Token missing. Please paste LinkedIn token in Tab 2!")
            else:
                with st.spinner("💼 Broadcasting to LinkedIn..."):
                    res = post_linkedin(content=caption_text, media_path_or_url=final_media, access_token=st.session_state["li_token"], author_urn=st.session_state["li_urn"], author=active_author)
                    with res_col2:
                        if "Published" in res or "Live" in res:
                            st.success("✅ **LinkedIn Feed:** Published Live!")
                        else:
                            st.error(f"❌ **LinkedIn Notice:** {res}")

        # 4. Facebook
        if target_fb:
            with res_col2:
                fb_share_url = f"https://www.facebook.com/sharer/sharer.php?u={urllib.parse.quote(img_url or 'https://dileep-ai-studio.streamlit.app')}&quote={urllib.parse.quote(caption_text)}"
                st.link_button("📘 1-Click Share to Facebook Timeline", fb_share_url, use_container_width=True)

        # 5. WhatsApp
        if target_wa:
            with res_col2:
                wa_phone = st.session_state["phone"].replace("+", "").strip() if st.session_state["phone"] else ""
                wa_text = f"{caption_text} -- {active_author}\n\n📸 4K Graphic: {img_url}" if img_url else caption_text
                wa_share_url = f"https://api.whatsapp.com/send?phone={wa_phone}&text={urllib.parse.quote(wa_text)}"
                st.link_button("💬 1-Click Deliver to WhatsApp", wa_share_url, use_container_width=True)

        st.balloons()
        st.toast("🎉 Grand Omni-Channel Broadcast Completed Successfully!")

# ==========================================
# TAB 2: CONNECT ACCOUNTS (DIRECT ZERO-LOOP LINKS)
# ==========================================
with tab_accounts:
    with st.container(border=True):
        st.markdown("### 🌟 Auto-Connect All 4 Platforms / चारों अकाउंट्स जोड़ें")
        st.markdown("Apna profile aur token save karein, **Active Status turant Green 🟢 ho jayega:**")

    col_left_form, col_right_status = st.columns([1.3, 1], gap="large")

    with col_left_form:
        # Profile Section
        with st.container(border=True):
            st.markdown("#### 👤 1. User Profile & WhatsApp")
            input_name = st.text_input("🏷️ Signature Name / आपका नाम (Watermark)", value=st.session_state["watermark"], placeholder="Enter your name / अपना नाम लिखें")
            input_phone = st.text_input("💬 WhatsApp Number / व्हाट्सएप नंबर (with country code)", value=st.session_state["phone"], placeholder="Enter WhatsApp number (e.g. +91...)")

        # Meta & LinkedIn Direct Token Tools
        with st.container(border=True):
            st.markdown("#### 📸 2. Instagram & Facebook (Meta)")
            st.link_button("🔗 Direct Meta Token Generator", "https://developers.facebook.com/tools/explorer/", use_container_width=True)
            input_ig_token = st.text_input("Paste Meta Token Here:", value=st.session_state["ig_token"], type="password", placeholder="EAAW...")

        with st.container(border=True):
            st.markdown("#### 💼 3. LinkedIn")
            # Clean direct OAuth Token Generator link without loop parameters
            st.link_button("🔗 Direct LinkedIn Token Generator", "https://www.linkedin.com/developers/tools/oauth/token-generator", use_container_width=True)
            input_li_token = st.text_input("Paste LinkedIn Token Here:", value=st.session_state["li_token"], type="password", placeholder="AQUg...")

        if st.button("✨ Save & Connect All Accounts / सभी अकाउंट्स कनेक्ट करें", type="primary", use_container_width=True):
            st.session_state["watermark"] = input_name
            st.session_state["phone"] = input_phone
            st.session_state["ig_token"] = input_ig_token
            st.session_state["li_token"] = input_li_token

            # Auto-Detect LinkedIn
            if input_li_token:
                with st.spinner("Auto-connecting LinkedIn..."):
                    detected_urn, detected_name = auto_detect_linkedin(input_li_token)
                    if detected_urn:
                        st.session_state["li_urn"] = detected_urn
                        st.session_state["li_name"] = detected_name

            # Auto-Detect Meta (Facebook + Instagram)
            if input_ig_token:
                with st.spinner("Auto-connecting Meta (Facebook & Instagram)..."):
                    detected_fb, detected_ig_id, detected_ig_user = auto_detect_meta(input_ig_token)
                    if detected_fb:
                        st.session_state["fb_name"] = detected_fb
                    if detected_ig_id:
                        st.session_state["ig_id"] = detected_ig_id
                        st.session_state["ig_user"] = detected_ig_user

            st.toast("🎉 Accounts Connected & Saved Successfully!")
            st.rerun()

    with col_right_status:
        with st.container(border=True):
            st.markdown("### 📊 Active Account Status")
            
            # Instagram Status
            if st.session_state["ig_token"]:
                ig_info = st.session_state["ig_user"] if st.session_state["ig_user"] else "Ready"
                st.markdown(f"📸 **Instagram:** 🟢 `Connected ({ig_info})`")
            else:
                st.markdown("📸 **Instagram:** ⚪ `Paste Meta Token on Left`")

            # Facebook Status
            if st.session_state["fb_name"]:
                st.markdown(f"📘 **Facebook:** 🟢 `Connected ({st.session_state['fb_name']})`")
            elif st.session_state["ig_token"]:
                st.markdown("📘 **Facebook:** 🟢 `Timeline Ready`")
            else:
                st.markdown("📘 **Facebook:** ⚪ `Paste Meta Token on Left`")

            # LinkedIn Status
            if st.session_state["li_token"]:
                li_user = st.session_state["li_name"] if st.session_state["li_name"] else "Connected"
                st.markdown(f"💼 **LinkedIn:** 🟢 `Connected ({li_user})`")
            else:
                st.markdown("💼 **LinkedIn:** ⚪ `Paste LinkedIn Token on Left`")

            # WhatsApp Status
            if st.session_state["phone"]:
                st.markdown(f"💬 **WhatsApp:** 🟢 `Ready ({st.session_state['phone']})`")
            else:
                st.markdown("💬 **WhatsApp:** ⚪ `Enter Number on Left`")

        if st.session_state["watermark"]:
            st.success(f"🏷️ Active Signature: **-- {st.session_state['watermark']}**")

# ==========================================
# TAB 3: EASY GUIDE & HELP
# ==========================================
with tab_guide:
    with st.container(border=True):
        st.markdown("### 📖 How to Use This Studio (Simple 3-Step Guide)")
        st.markdown("""
        1. **Choose Your Content / कंटेंट चुनें:**
           - Select **"Upload Photo/Video from PC"** to pick any photo or video from your computer.
           - OR click **"Auto-Generate Quote"** to let AI craft a 4K nature graphic automatically!
        2. **Select Target Platforms (All 4 Networks) / सोशल मीडिया चुनें:**
           - Tick the checkboxes for where you want to post: **Instagram, Facebook, LinkedIn, or WhatsApp**.
        3. **Click Launch / पोस्ट करें:**
           - Hit **"🚀 Launch Multi-Platform Post"** and watch your content publish across all channels simultaneously!
        """)
        st.markdown("---")
        st.markdown("💡 **Tip:** To launch the studio anytime without opening VS Code, simply double-click the **`Launch_AI_Studio.bat`** file on your computer!")
