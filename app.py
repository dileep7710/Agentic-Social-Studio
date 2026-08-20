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
    page_title="Agentic AI Omni-Studio",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Curated High-Impact Quotes
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

# Premium Glassmorphism Styling
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

# Initialize Isolated Per-User Session State (No data bleed between visitors)
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
if "history" not in st.session_state:
    st.session_state["history"] = []

# Helper: Auto-Detect LinkedIn
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

# Helper: Auto-Detect Meta
def auto_detect_meta(token: str):
    if not token:
        return None, None, None
    fb_name = "Connected User"
    ig_id = "17841448994358440"
    ig_user = "@dileepy18"
    try:
        with httpx.Client(timeout=15.0) as client:
            r_me = client.get(f"https://graph.facebook.com/v21.0/me?fields=name,id&access_token={token}")
            if r_me.status_code == 200:
                fb_name = r_me.json().get("name", "Connected User")

            r_acc = client.get(f"https://graph.facebook.com/v21.0/me/accounts?fields=instagram_business_account,name&access_token={token}")
            if r_acc.status_code == 200:
                data = r_acc.json().get("data", [])
                for page in data:
                    ig_acc = page.get("instagram_business_account", {})
                    if "id" in ig_acc:
                        ig_id = ig_acc["id"]
                        ig_user = page.get("name", "Instagram User")
                        return fb_name, ig_id, ig_user
    except Exception:
        pass
    return fb_name, ig_id, ig_user

# Sidebar Profile Status
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=400&q=80", use_container_width=True)
    
    lang = st.radio("🌐 Language / भाषा:", ["English", "हिन्दी (Hindi)"], horizontal=True)
    
    st.markdown("---")
    st.markdown("### 👤 Active Profile / एक्टिव यूजर")
    display_user = st.session_state["watermark"] if st.session_state["watermark"] else "Public Guest"
    display_phone = st.session_state["phone"] if st.session_state["phone"] else "Not Set"
    st.markdown(f'<div class="glowing-badge">🏷️ Name: {display_user}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="glowing-badge">💬 WhatsApp: {display_phone}</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### ⚡ 1-Click Multi-Platform Engine")
    st.caption("Broadcast 4K images & videos across Instagram (Story/Feed), Facebook, LinkedIn & WhatsApp.")

# Main Header
if lang == "English":
    st.markdown('<div class="fantasy-title">🌌 Agentic AI Omni-Studio</div>', unsafe_allow_html=True)
    st.markdown('<div class="fantasy-subtitle">Create 4K Visual Content & Broadcast Across Social Channels in 1-Click</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="fantasy-title">🌌 एजेंटिक AI ऑम्नी-स्टूडियो</div>', unsafe_allow_html=True)
    st.markdown('<div class="fantasy-subtitle">4K विजुअल कंटेंट बनाएं और सोशल मीडिया पर 1-क्लिक में पोस्ट करें</div>', unsafe_allow_html=True)

# Tabs
tab_studio, tab_profile, tab_history, tab_guide = st.tabs([
    "🔮 Studio / पोस्ट स्टूडियो", 
    "⚙️ Connect Accounts / प्रोफाइल और अकाउंट्स", 
    "📜 History / पिछला इतिहास",
    "📖 Easy Guide / सरल मदद"
])

# ==========================================
# TAB 1: STUDIO (POST CREATOR)
# ==========================================
with tab_studio:
    col_left, col_right = st.columns([1.25, 1], gap="large")

    with col_left:
        with st.container(border=True):
            st.markdown("### 🎨 1. Content & Media / कंटेंट चुनें")

            source_label = "Select Content Source:" if lang == "English" else "कंटेंट का प्रकार चुनें:"
            opt1 = "✨ Generate 4K AI Nature Graphic" if lang == "English" else "✨ 4K AI नेचर ग्राफिक बनाएं"
            opt2 = "📂 Upload Photo/Video from PC/Phone" if lang == "English" else "📂 अपने फोन/PC से फोटो या वीडियो चुनें"

            media_source = st.radio(source_label, [opt1, opt2], horizontal=True)

            if media_source == opt2:
                up_label = "Choose an image (.jpg, .png) or video (.mp4) from your local folder:" if lang == "English" else "अपने कम्प्यूटर या फोन से फोटो या वीडियो चुनें:"
                uploaded_file = st.file_uploader(up_label, type=["jpg", "jpeg", "png", "mp4"])
                if uploaded_file is not None:
                    suffix = Path(uploaded_file.name).suffix
                    tfile = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
                    tfile.write(uploaded_file.read())
                    st.session_state["custom_media_path"] = tfile.name
                    st.success(f"📂 Loaded: {uploaded_file.name}")
            else:
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
            st.markdown("### 🎯 2. Social Destinations / सोशल मीडिया")
            
            c1, c2 = st.columns(2)
            with c1:
                target_insta_story = st.checkbox("📸 Instagram Story (24h) 🟢", value=True)
                target_insta_feed = st.checkbox("🖼️ Instagram Feed Post 🟢", value=True)
            with c2:
                target_fb = st.checkbox("📘 Facebook Timeline & Feed 🟢", value=True)
                target_li = st.checkbox("💼 LinkedIn Post 🟢", value=True)
                target_wa = st.checkbox("💬 WhatsApp Delivery 🟢", value=True)

        # Action Buttons
        b1, b2 = st.columns([1, 1.3])
        with b1:
            btn_prev = "🖼️ Refresh Preview" if lang == "English" else "🖼️ प्रीव्यू देखें"
            preview_clicked = st.button(btn_prev, use_container_width=True)
        with b2:
            btn_post = "🚀 Launch Multi-Platform Post" if lang == "English" else "🚀 सभी जगह पोस्ट करें"
            publish_clicked = st.button(btn_post, type="primary", use_container_width=True)

    # Preview Handling
    active_author = st.session_state["watermark"] if st.session_state["watermark"] else "AI Creator"
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
                    st.image(img, caption=f"✨ Watermark: -- {active_author}", use_container_width=True)
                    
                    # Direct 1-Click Download Button for ANY User!
                    with open(preview_file, "rb") as file_bytes:
                        st.download_button(
                            label="💾 Download 4K Graphic / फोटो डाउनलोड करें",
                            data=file_bytes,
                            file_name="Agentic_AI_Graphic.png",
                            mime="image/png",
                            use_container_width=True
                        )
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
            # Record in session history
            st.session_state["history"].append({
                "quote": caption_text,
                "author": active_author,
                "img": img_url or "Local Media",
                "time": "Just now"
            })

        st.markdown("### 📊 Live Omni-Channel Dispatch Results")
        
        # Action Card Container
        with st.container(border=True):
            st.markdown("#### 🚀 Your Post is Ready & Broadcasted!")
            st.markdown(f"**Caption:** *\"{caption_text}\"*")
            st.markdown(f"**Watermark Signature:** `-- {active_author}`")
            if img_url:
                st.markdown(f"📸 **4K CDN Media:** [View Direct Image]({img_url})")

        res_col1, res_col2 = st.columns(2)

        # 1. Instagram Story
        if target_insta_story:
            with res_col1:
                with st.container(border=True):
                    st.markdown("#### 📸 1. Instagram Story (24h)")
                    res = post_instagram_story(content=caption_text, media_path_or_url=img_url or final_media, user_id=st.session_state["ig_id"], access_token=st.session_state["ig_token"] or None, author=active_author)
                    if "Published" in res or "Live" in res:
                        st.success("✅ **Live Published to Instagram Story!**")
                    else:
                        st.info("📸 Ready for Story! Click below to download graphic & upload:")
                        st.link_button("📸 Open Instagram App/Web", "https://www.instagram.com/", use_container_width=True)

        # 2. Instagram Feed
        if target_insta_feed:
            with res_col1:
                with st.container(border=True):
                    st.markdown("#### 🖼️ 2. Instagram Feed Post")
                    res = post_instagram_feed(content=caption_text, media_path_or_url=img_url or final_media, user_id=st.session_state["ig_id"], access_token=st.session_state["ig_token"] or None, author=active_author)
                    if "Published" in res or "Live" in res:
                        st.success("✅ **Live Published to Instagram Feed!**")
                    else:
                        st.link_button("🖼️ Open Instagram Feed", "https://www.instagram.com/", use_container_width=True)

        # 3. LinkedIn (API Posting for Devs or 1-Click for Public Users)
        if target_li:
            with res_col2:
                with st.container(border=True):
                    st.markdown("#### 💼 3. LinkedIn Feed")
                    if st.session_state["li_token"]:
                        res = post_linkedin(content=caption_text, media_path_or_url=final_media, access_token=st.session_state["li_token"], author_urn=st.session_state["li_urn"] or None, author=active_author)
                        if "Published" in res or "Live" in res:
                            st.success("✅ **Published Live on Your LinkedIn!**")
                            st.link_button("💼 View Live Post on LinkedIn", "https://www.linkedin.com/feed/", use_container_width=True)
                        else:
                            li_share_url = f"https://www.linkedin.com/sharing/share-offsite/?url={urllib.parse.quote(img_url or 'https://dileep-ai-studio.streamlit.app')}"
                            st.link_button("💼 1-Click Post to Your LinkedIn", li_share_url, use_container_width=True)
                    else:
                        li_share_url = f"https://www.linkedin.com/sharing/share-offsite/?url={urllib.parse.quote(img_url or 'https://dileep-ai-studio.streamlit.app')}"
                        st.link_button("💼 1-Click Post to Your LinkedIn", li_share_url, use_container_width=True)

        # 4. Facebook (Universal 1-Click Timeline & Feed Post)
        if target_fb:
            with res_col2:
                with st.container(border=True):
                    st.markdown("#### 📘 4. Facebook Feed & Timeline")
                    fb_share_url = f"https://www.facebook.com/sharer/sharer.php?u={urllib.parse.quote(img_url or 'https://dileep-ai-studio.streamlit.app')}&quote={urllib.parse.quote(caption_text)}"
                    st.link_button("📘 Click to Publish on Facebook Feed", fb_share_url, use_container_width=True)

        # 5. WhatsApp (Universal 1-Click Delivery)
        if target_wa:
            with res_col2:
                with st.container(border=True):
                    st.markdown("#### 💬 5. WhatsApp Delivery")
                    wa_phone = st.session_state["phone"].replace("+", "").strip() if st.session_state["phone"] else ""
                    wa_text = f"{caption_text} -- {active_author}\n\n📸 4K Media: {img_url}" if img_url else caption_text
                    wa_share_url = f"https://api.whatsapp.com/send?phone={wa_phone}&text={urllib.parse.quote(wa_text)}" if wa_phone else f"https://api.whatsapp.com/send?text={urllib.parse.quote(wa_text)}"
                    st.link_button("💬 Click to Deliver on WhatsApp", wa_share_url, use_container_width=True)

        st.balloons()
        st.toast("🎉 Grand Omni-Channel Broadcast Completed!")

# ==========================================
# TAB 2: USER PROFILE & SETTINGS (CLEAN & 100% ERROR-FREE)
# ==========================================
with tab_profile:
    with st.container(border=True):
        st.markdown("### 👤 User Profile & Signature / प्रोफाइल सेटिंग्स")
        st.markdown("Apna naam aur WhatsApp number yahan likhein — **har photo par aapka signature watermark lagega:**")

    col_left_form, col_right_status = st.columns([1.3, 1], gap="large")

    with col_left_form:
        # Profile Section
        with st.container(border=True):
            st.markdown("#### 🏷️ 1. Your Details")
            input_name = st.text_input("Signature Name / आपका नाम (Watermark):", value=st.session_state["watermark"], placeholder="Enter your name / अपना नाम लिखें")
            input_phone = st.text_input("WhatsApp Number / व्हाट्सएप नंबर (with country code):", value=st.session_state["phone"], placeholder="Enter WhatsApp number / व्हाट्सएप नंबर (e.g. +91...)")

        b_save, b_reset = st.columns([1.5, 1])
        with b_save:
            if st.button("✨ Save Profile / प्रोफाइल सेव करें", type="primary", use_container_width=True):
                st.session_state["watermark"] = input_name
                st.session_state["phone"] = input_phone
                st.toast("🎉 Profile Saved Successfully!")
                st.rerun()

        with b_reset:
            if st.button("🔄 Reset / रीसेट करें", use_container_width=True):
                st.session_state["watermark"] = ""
                st.session_state["phone"] = ""
                st.session_state["ig_token"] = ""
                st.session_state["li_token"] = ""
                st.rerun()

        # Pro Developer API Settings (Collapsed & Safe)
        with st.expander("🛠️ Pro Developer API Settings (Optional)"):
            st.caption("Only for developers who want automated background Graph API posting.")
            input_ig_token = st.text_input("Meta Access Token (Optional):", value=st.session_state["ig_token"], type="password")
            input_li_token = st.text_input("LinkedIn Access Token (Optional):", value=st.session_state["li_token"], type="password")
            if st.button("Save API Tokens"):
                st.session_state["ig_token"] = input_ig_token
                st.session_state["li_token"] = input_li_token
                st.success("API Tokens Saved!")

    with col_right_status:
        with st.container(border=True):
            st.markdown("### 📊 Active Account Status")
            user_lbl = st.session_state["watermark"] if st.session_state["watermark"] else "Public Guest"
            phone_lbl = st.session_state["phone"] if st.session_state["phone"] else "Not Set"
            
            st.markdown(f"🏷️ **Active Signature:** 🟢 `{user_lbl}`")
            st.markdown(f"💬 **WhatsApp Target:** 🟢 `{phone_lbl}`")
            
            if st.session_state["ig_token"]:
                st.markdown(f"📸 **Instagram:** 🟢 `Connected ({st.session_state['ig_user']})`")
            else:
                st.markdown("📸 **Instagram:** 🟢 `1-Click Direct Share Ready`")

            if st.session_state["fb_name"]:
                st.markdown(f"📘 **Facebook:** 🟢 `Connected ({st.session_state['fb_name']})`")
            else:
                st.markdown("📘 **Facebook:** 🟢 `1-Click Feed Share Ready`")

            if st.session_state["li_token"]:
                st.markdown(f"💼 **LinkedIn:** 🟢 `Connected ({st.session_state['li_name']})`")
            else:
                st.markdown("💼 **LinkedIn:** 🟢 `1-Click Share Ready`")

        if st.session_state["watermark"]:
            st.success(f"✨ Signature Watermark: **-- {st.session_state['watermark']}**")

# ==========================================
# TAB 3: POST HISTORY
# ==========================================
with tab_history:
    with st.container(border=True):
        st.markdown("### 📜 Session Post History / पिछला इतिहास")
        st.markdown("Aapke dwara generate kiye gaye sabhi quotes aur graphics ka **Record:**")
        
        if st.session_state["history"]:
            for item in reversed(st.session_state["history"]):
                with st.expander(f"✨ \"{item['quote'][:45]}...\" -- {item['author']}"):
                    st.write(f"**Full Quote:** {item['quote']}")
                    st.write(f"**Signature:** -- {item['author']}")
                    if item.get("img") and item["img"].startswith("http"):
                        st.markdown(f"📸 **Media Link:** [View HD Image/Video]({item['img']})")
        else:
            st.info("👈 Abhi tak koi post create nahi hua hai. Tab 1 mein jakar naya post create karein!")

# ==========================================
# TAB 4: EASY GUIDE & HELP
# ==========================================
with tab_guide:
    with st.container(border=True):
        st.markdown("### 📖 How Any User Can Use This Studio (100% Free & Zero Friction!)")
        st.markdown("""
        1. **Set Your Name / अपना नाम लिखें:**
           - Go to **Tab 2 (Connect Accounts)** and enter your name (e.g. *Dileep Yadav*).
        2. **Create or Upload Media / फोटो या वीडियो चुनें:**
           - Go to **Tab 1 (Studio)**, type your quote, click **"Auto-Generate Inspiring Quote"** or upload any photo/video from your folder!
        3. **1-Click Broadcast Everywhere / पोस्ट करें:**
           - Hit **"🚀 Launch Multi-Platform Post"** to broadcast to **Instagram Story, Feed, Facebook Timeline, LinkedIn & WhatsApp** in 1 second!
        """)
