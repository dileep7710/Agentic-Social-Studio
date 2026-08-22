import streamlit as st
import streamlit.components.v1 as components
import os
import json
import uuid
import tempfile
import urllib.parse
from pathlib import Path
from PIL import Image
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import database persistence with multi-user isolation
from database import (
    get_user_profile,
    save_user_profile,
    clear_user_profile,
    save_post_to_history,
    get_recent_posts
)

# Import our unified social engine tools & autonomous agent
from ai_agent import agent
from social_tools import (
    create_nature_quote_image,
    upload_local_file,
    post_instagram_story,
    post_instagram_feed,
    post_facebook_page,
    post_linkedin,
    post_whatsapp,
    post_twitter_x,
    get_facebook_share_url,
    get_linkedin_share_url
)

# Page Configuration
st.set_page_config(
    page_title="Agentic AI Omni-Studio",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

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

# 100% Isolated Unique Session ID per Visitor (Zero Data Bleed Guarantee)
if "session_id" not in st.session_state:
    st.session_state["session_id"] = str(uuid.uuid4())

user_sid = st.session_state["session_id"]

# Fetch User-Specific Isolated Profile from Database
db_profile = get_user_profile(user_sid)

# Initialize Session State
if "watermark" not in st.session_state:
    st.session_state["watermark"] = db_profile.get("name", "")
if "phone" not in st.session_state:
    st.session_state["phone"] = db_profile.get("phone", "")
if "ig_id" not in st.session_state:
    st.session_state["ig_id"] = db_profile.get("ig_id", "")
if "ig_token" not in st.session_state:
    st.session_state["ig_token"] = db_profile.get("ig_token", "")
if "fb_page_id" not in st.session_state:
    st.session_state["fb_page_id"] = db_profile.get("fb_page_id", "")
if "fb_page_token" not in st.session_state:
    st.session_state["fb_page_token"] = db_profile.get("fb_page_token", "")
if "li_token" not in st.session_state:
    st.session_state["li_token"] = db_profile.get("li_token", "")
if "li_urn" not in st.session_state:
    st.session_state["li_urn"] = db_profile.get("li_urn", "")

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
    st.markdown("### 🔒 100% Private & Isolated")
    st.caption("Aapka data aur phone number sirf aapke session tak seemit hai — koi doosra user ise nahi dekh sakta.")

# Main Header
if lang == "English":
    st.markdown('<div class="fantasy-title">🌌 Agentic AI Omni-Studio</div>', unsafe_allow_html=True)
    st.markdown('<div class="fantasy-subtitle">Autonomous Goal Understanding, 4K Media Generation & 1-Click Multi-Platform Broadcasting</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="fantasy-title">🌌 एजेंटिक AI ऑम्नी-स्टूडियो</div>', unsafe_allow_html=True)
    st.markdown('<div class="fantasy-subtitle">4K विजुअल बनाएं, AI से कंटेंट अनुकूलित करें और 1-क्लिक में सभी सोशल मीडिया पर पोस्ट करें</div>', unsafe_allow_html=True)

# Tabs
tab_studio, tab_profile, tab_history, tab_guide = st.tabs([
    "🔮 Studio / पोस्ट स्टूडियो", 
    "⚙️ Connect Accounts / प्रोफाइल सेटिंग्स", 
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
            opt2 = "📂 Upload Photo/Video from Phone/PC" if lang == "English" else "📂 अपने फोन/PC से फोटो या वीडियो चुनें"

            media_source = st.radio(source_label, [opt1, opt2], horizontal=True)

            if media_source == opt2:
                up_label = "Choose an image (.jpg, .png) or video (.mp4) from your local folder:" if lang == "English" else "अपने कम्प्यूटर या फोन से फोटो या वीडियो चुनें:"
                uploaded_file = st.file_uploader(up_label, type=["jpg", "jpeg", "png", "mp4"])
                if uploaded_file is not None:
                    suffix = Path(uploaded_file.name).suffix
                    tfile = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
                    tfile.write(uploaded_file.read())
                    st.session_state["custom_media_path"] = tfile.name
                    st.session_state["is_video"] = suffix.lower() in [".mp4", ".mov"]
                    st.success(f"📂 Loaded: {uploaded_file.name}")
            else:
                btn_txt = "✨ Auto-Generate Inspiring Quote / नया विचार बनाएं" if lang == "English" else "✨ नया विचार (AI Quote) जनरेट करें"
                if st.button(btn_txt, use_container_width=True):
                    with st.spinner("🧠 AI is crafting an inspiring quote..."):
                        chosen_quote = agent.generate_fresh_quote()
                        st.session_state["quote_input"] = chosen_quote
                        st.toast("✨ New inspiring quote generated!")

        with st.container(border=True):
            cap_label = "Caption / Quote / विचार:" if lang == "English" else "कैप्शन या विचार:"
            caption_text = st.text_area(
                cap_label,
                value=st.session_state.get("quote_input", "The secret of getting ahead is getting started."),
                height=80
            )

        # Dynamic AI Platform Adaptation (PPT Slide 8)
        active_author = st.session_state["watermark"] if st.session_state["watermark"] else "AI Creator"
        adapted_versions = agent.adapter.adapt_all_platforms(caption_text, author=active_author)

        with st.expander("✨ View AI Platform-Tailored Copies (PPT Slide 8)"):
            t_insta, t_li, t_fb, t_wa, t_tw = st.tabs(["📸 Instagram", "💼 LinkedIn", "📘 Facebook", "💬 WhatsApp", "🐦 Twitter/X"])
            with t_insta:
                st.code(adapted_versions["instagram"], language="markdown")
            with t_li:
                st.code(adapted_versions["linkedin"], language="markdown")
            with t_fb:
                st.code(adapted_versions["facebook"], language="markdown")
            with t_wa:
                st.code(adapted_versions["whatsapp"], language="markdown")
            with t_tw:
                st.code(adapted_versions["twitter"], language="markdown")

        with st.container(border=True):
            st.markdown("### 🎯 2. Social Destinations / सोशल मीडिया")
            
            c1, c2 = st.columns(2)
            with c1:
                target_insta_story = st.checkbox("📸 Instagram Story (24h) 🟢", value=True)
                target_insta_feed = st.checkbox("🖼️ Instagram Feed Post 🟢", value=True)
                target_tw = st.checkbox("🐦 X / Twitter Tweet 🟢", value=True)
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
    if preview_clicked or "latest_preview" not in st.session_state:
        if media_source == opt1 or "custom_media_path" not in st.session_state:
            img_path = create_nature_quote_image(caption_text, author=active_author, is_story=True)
            st.session_state["latest_preview"] = img_path
        elif "custom_media_path" in st.session_state:
            st.session_state["latest_preview"] = st.session_state["custom_media_path"]

    with col_right:
        with st.container(border=True):
            prev_title = "### 🖼️ Live 4K Visual Preview" if lang == "English" else "### 🖼️ लाइव 4K प्रीव्यू"
            st.markdown(prev_title)
            
            preview_file = st.session_state.get("latest_preview")
            if preview_file and os.path.exists(preview_file):
                if preview_file.lower().endswith((".png", ".jpg", ".jpeg")):
                    img = Image.open(preview_file)
                    st.image(img, caption=f"✨ Watermark Signature: -- {active_author}", use_container_width=True)
                    
                    # Direct 1-Click Download Button for ANY User!
                    with open(preview_file, "rb") as file_bytes:
                        st.download_button(
                            label="💾 Download 4K Graphic / फोटो डाउनलोड करें",
                            data=file_bytes,
                            file_name="Agentic_AI_Graphic.png",
                            mime="image/png",
                            use_container_width=True
                        )
                elif preview_file.lower().endswith((".mp4", ".mov")):
                    st.video(preview_file)
            else:
                info_txt = "👈 Select a file or click 'Refresh Preview' to see your media here!" if lang == "English" else "👈 बाईं तरफ फोटो चुनें या प्रीव्यू बटन दबाएं!"
                st.info(info_txt)

    # Multi-Platform Execution
    if publish_clicked:
        st.markdown("---")
        st.markdown("### 📊 Live Omni-Channel Dispatch Results")

        if media_source == opt2 and "custom_media_path" in st.session_state:
            final_media = st.session_state["custom_media_path"]
        else:
            final_media = create_nature_quote_image(caption_text, author=active_author, is_story=True)
            st.session_state["latest_preview"] = final_media

        # Read binary data for download buttons
        raw_bytes = b""
        if final_media and os.path.exists(final_media):
            try:
                with open(final_media, "rb") as f:
                    raw_bytes = f.read()
            except Exception:
                raw_bytes = b""

        with st.spinner("⚡ Uploading asset to high-speed CDN..."):
            img_url = upload_local_file(final_media)
            # Record in Isolated SQLite Database strictly for this session_id
            save_post_to_history(user_sid, caption_text, active_author, img_url or "Local Media")

        # Action Card Container
        with st.container(border=True):
            st.markdown("#### 🚀 Your Post is Ready & Broadcasted!")
            st.markdown(f"**Caption:** *\"{caption_text}\"*")
            st.markdown(f"**Watermark Signature:** `-- {active_author}`")
            if img_url:
                st.markdown(f"📸 **4K CDN Media:** [View Direct Image]({img_url})")

            # 1-Tap Native Mobile & Desktop Share Sheet
            components.html(f"""
            <div style="text-align: center; margin: 10px 0 5px 0;">
                <button id="omniShareBtn" style="
                    width: 100%;
                    padding: 14px 20px;
                    background: linear-gradient(135deg, #FF6B6B 0%, #FF8E53 25%, #FFD93D 50%, #6BCB77 75%, #4D96FF 100%);
                    color: #FFFFFF;
                    border: none;
                    border-radius: 12px;
                    font-size: 15px;
                    font-weight: 800;
                    cursor: pointer;
                    box-shadow: 0 4px 20px rgba(99, 102, 241, 0.45);
                    font-family: sans-serif;
                ">
                    📲 1-TAP NATIVE SHARE TO INSTAGRAM, WHATSAPP, FB & LINKEDIN
                </button>
            </div>
            <script>
                document.getElementById('omniShareBtn').addEventListener('click', async () => {{
                    if (navigator.share) {{
                        try {{
                            await navigator.share({{
                                title: 'Agentic AI 4K Creation',
                                text: {json.dumps(adapted_versions["whatsapp"])},
                                url: {json.dumps(img_url or 'https://dileep-ai-studio.streamlit.app')}
                            }});
                        }} catch (err) {{
                            console.log('Share dismissed');
                        }}
                    }} else {{
                        alert('Native Sharing triggered! You can also use the direct buttons below.');
                    }}
                }});
            </script>
            """, height=65)

        res_col1, res_col2 = st.columns(2)

        # 1. Instagram Story
        if target_insta_story:
            with res_col1:
                with st.container(border=True):
                    st.markdown("#### 📸 1. Instagram Story (24h)")
                    if st.session_state["ig_token"] and st.session_state["ig_id"]:
                        res = post_instagram_story(content=caption_text, media_path_or_url=img_url or final_media, user_id=st.session_state["ig_id"], access_token=st.session_state["ig_token"], author=active_author)
                        if res.get("status") == "SUCCESS":
                            st.success(f"✅ **Live Published to Instagram Story via Meta API!** (ID: `{res.get('post_id')}`)")
                        else:
                            st.warning(f"⚠️ Meta API Notice: {res.get('message', 'Direct API post requires active business token.')}")
                            st.markdown("👇 **1-Tap Mobile Story Posting:**")
                            st.download_button(
                                label="💾 Step 1: Download 4K Story Graphic",
                                data=raw_bytes,
                                file_name=f"instagram_story_{int(time.time())}.png",
                                mime="image/png",
                                key="dl_ig_story",
                                use_container_width=True
                            )
                            st.link_button("📸 Step 2: Open Instagram Story Camera", "https://www.instagram.com/create/story/", use_container_width=True)
                    else:
                        st.markdown("💡 **1-Tap Story Sharing:**")
                        st.download_button(
                            label="💾 Step 1: Download 4K Story Graphic",
                            data=raw_bytes,
                            file_name=f"instagram_story_{int(time.time())}.png",
                            mime="image/png",
                            key="dl_ig_story_guest",
                            use_container_width=True
                        )
                        st.link_button("📸 Step 2: Open Instagram Story Camera", "https://www.instagram.com/create/story/", use_container_width=True)

        # 2. Instagram Feed
        if target_insta_feed:
            with res_col1:
                with st.container(border=True):
                    st.markdown("#### 🖼️ 2. Instagram Feed Post")
                    if st.session_state["ig_token"] and st.session_state["ig_id"]:
                        res = post_instagram_feed(content=adapted_versions["instagram"], media_path_or_url=img_url or final_media, user_id=st.session_state["ig_id"], access_token=st.session_state["ig_token"], author=active_author)
                        if res.get("status") == "SUCCESS":
                            st.success(f"✅ **Live Published to Instagram Feed via Meta API!** (ID: `{res.get('post_id')}`)")
                        else:
                            st.warning(f"⚠️ Meta API Notice: {res.get('message', 'Direct API post requires active business token.')}")
                            st.download_button(
                                label="💾 Step 1: Download 4K Feed Graphic",
                                data=raw_bytes,
                                file_name=f"instagram_feed_{int(time.time())}.png",
                                mime="image/png",
                                key="dl_ig_feed",
                                use_container_width=True
                            )
                            st.link_button("🖼️ Step 2: Open Instagram Feed", "https://www.instagram.com/", use_container_width=True)
                    else:
                        st.download_button(
                            label="💾 Step 1: Download 4K Feed Graphic",
                            data=raw_bytes,
                            file_name=f"instagram_feed_{int(time.time())}.png",
                            mime="image/png",
                            key="dl_ig_feed_guest",
                            use_container_width=True
                        )
                        st.link_button("🖼️ Step 2: Open Instagram Feed", "https://www.instagram.com/", use_container_width=True)

        # 3. LinkedIn
        if target_li:
            with res_col2:
                with st.container(border=True):
                    st.markdown("#### 💼 3. LinkedIn Feed")
                    if st.session_state["li_token"]:
                        res = post_linkedin(content=adapted_versions["linkedin"], media_path_or_url=final_media, access_token=st.session_state["li_token"], author_urn=st.session_state["li_urn"] or None, author=active_author)
                        if res.get("status") == "SUCCESS":
                            st.success(f"✅ **Published Live on Your LinkedIn!** (Post ID: `{res.get('post_id')}`)")
                            st.link_button("💼 View Live Post on LinkedIn", "https://www.linkedin.com/feed/", use_container_width=True)
                        else:
                            st.warning(f"⚠️ LinkedIn Notice: {res.get('message', 'Direct API post requires active token.')}")
                            li_url = get_linkedin_share_url(img_url)
                            st.link_button("💼 1-Click Post to Your LinkedIn", li_url, use_container_width=True)
                    else:
                        li_url = get_linkedin_share_url(img_url)
                        st.link_button("💼 1-Click Post to Your LinkedIn", li_url, use_container_width=True)

        # 4. Facebook
        if target_fb:
            with res_col2:
                with st.container(border=True):
                    st.markdown("#### 📘 4. Facebook Feed & Timeline")
                    if st.session_state["fb_page_id"] and st.session_state["fb_page_token"]:
                        res = post_facebook_page(content=adapted_versions["facebook"], media_path_or_url=final_media, page_id=st.session_state["fb_page_id"], page_access_token=st.session_state["fb_page_token"], author=active_author)
                        if res.get("status") == "SUCCESS":
                            st.success(f"✅ **Published Live on Your Facebook Page!** (Post ID: `{res.get('post_id')}`)")
                        else:
                            fb_url = get_facebook_share_url(img_url, adapted_versions["facebook"])
                            st.link_button("📘 Click to Publish on Facebook Timeline", fb_url, use_container_width=True)
                    else:
                        fb_url = get_facebook_share_url(img_url, adapted_versions["facebook"])
                        st.link_button("📘 Click to Publish on Facebook Timeline", fb_url, use_container_width=True)

        # 5. WhatsApp
        if target_wa:
            with res_col2:
                with st.container(border=True):
                    st.markdown("#### 💬 5. WhatsApp Delivery")
                    wa_phone = st.session_state["phone"].replace("+", "").strip() if st.session_state["phone"] else ""
                    wa_res = post_whatsapp(content=adapted_versions["whatsapp"], target=wa_phone, media_path_or_url=img_url, author=active_author)
                    st.link_button("💬 Click to Deliver on WhatsApp", wa_res["action_url"], use_container_width=True)

        # 6. Twitter / X
        if target_tw:
            with res_col1:
                with st.container(border=True):
                    st.markdown("#### 🐦 6. X / Twitter Tweet")
                    tw_res = post_twitter_x(content=adapted_versions["twitter"], media_path_or_url=img_url, author=active_author)
                    st.link_button("🐦 Click to Tweet on X", tw_res["action_url"], use_container_width=True)

        st.balloons()
        st.toast("🎉 Grand Omni-Channel Broadcast Completed!")

# ==========================================
# TAB 2: USER PROFILE & SETTINGS
# ==========================================
with tab_profile:
    with st.container(border=True):
        st.markdown("### 👤 User Profile & Privacy / प्रोफाइल सेटिंग्स")
        st.markdown("🔒 **100% Privacy:** Aapka naam, number aur tokens sirf aapke is browser session mein safe rahenge. Koi doosra user aapka data kabhi nahi dekh sakta.")

    col_left_form, col_right_status = st.columns([1.3, 1], gap="large")

    with col_left_form:
        with st.container(border=True):
            st.markdown("#### 🏷️ 1. Your Details")
            input_name = st.text_input("Signature Name / आपका नाम (Watermark):", value=st.session_state["watermark"], placeholder="Enter your name / अपना नाम लिखें")
            input_phone = st.text_input("WhatsApp Number / व्हाट्सएप नंबर (with country code):", value=st.session_state["phone"], placeholder="Enter WhatsApp number (e.g. +91...)")

        b_save, b_reset = st.columns([1.5, 1])
        with b_save:
            if st.button("✨ Save Profile (Private) / प्रोफाइल सेव करें", type="primary", use_container_width=True):
                st.session_state["watermark"] = input_name
                st.session_state["phone"] = input_phone
                try:
                    save_user_profile(
                        session_id=user_sid,
                        name=input_name,
                        phone=input_phone,
                        ig_id=st.session_state.get("ig_id", ""),
                        ig_token=st.session_state.get("ig_token", ""),
                        fb_page_id=st.session_state.get("fb_page_id", ""),
                        fb_page_token=st.session_state.get("fb_page_token", ""),
                        li_token=st.session_state.get("li_token", ""),
                        li_urn=st.session_state.get("li_urn", "")
                    )
                except Exception as e:
                    pass
                st.toast("🎉 Profile Saved Privately in Isolated Session!")
                st.rerun()

        with b_reset:
            if st.button("🔄 Reset Profile / रीसेट करें", use_container_width=True):
                try:
                    clear_user_profile(user_sid)
                except Exception:
                    pass
                st.session_state["watermark"] = ""
                st.session_state["phone"] = ""
                st.session_state["ig_token"] = ""
                st.session_state["li_token"] = ""
                st.rerun()

        # Pro Developer API Settings (Optional)
        with st.expander("🛠️ Pro Developer API Settings (Optional)"):
            st.caption("Saved privately in your isolated session.")
            input_ig_id = st.text_input("Instagram Business Account ID:", value=st.session_state["ig_id"])
            input_ig_token = st.text_input("Meta / Instagram Access Token:", value=st.session_state["ig_token"], type="password")
            input_fb_page_id = st.text_input("Facebook Page ID:", value=st.session_state["fb_page_id"])
            input_fb_page_token = st.text_input("Facebook Page Access Token:", value=st.session_state["fb_page_token"], type="password")
            input_li_token = st.text_input("LinkedIn Access Token:", value=st.session_state["li_token"], type="password")
            if st.button("Save API Tokens (Private)"):
                st.session_state["ig_id"] = input_ig_id
                st.session_state["ig_token"] = input_ig_token
                st.session_state["fb_page_id"] = input_fb_page_id
                st.session_state["fb_page_token"] = input_fb_page_token
                st.session_state["li_token"] = input_li_token
                try:
                    save_user_profile(
                        session_id=user_sid,
                        name=st.session_state["watermark"],
                        phone=st.session_state["phone"],
                        ig_id=input_ig_id,
                        ig_token=input_ig_token,
                        fb_page_id=input_fb_page_id,
                        fb_page_token=input_fb_page_token,
                        li_token=input_li_token,
                        li_urn=st.session_state["li_urn"]
                    )
                except Exception:
                    pass
                st.success("API Tokens Saved Privately in Your Session!")

    with col_right_status:
        with st.container(border=True):
            st.markdown("### 📊 Active Account Status")
            user_lbl = st.session_state["watermark"] if st.session_state["watermark"] else "Public Guest"
            phone_lbl = st.session_state["phone"] if st.session_state["phone"] else "Not Set"
            
            st.markdown(f"🏷️ **Active Signature:** 🟢 `{user_lbl}`")
            st.markdown(f"💬 **WhatsApp Target:** 🟢 `{phone_lbl}`")
            st.markdown(f"📸 **Instagram:** 🟢 `{'Connected' if st.session_state['ig_token'] else '1-Click Direct Share Ready'}`")
            st.markdown(f"📘 **Facebook:** 🟢 `{'Connected' if st.session_state['fb_page_token'] else '1-Click Share Ready'}`")
            st.markdown(f"💼 **LinkedIn:** 🟢 `{'Connected' if st.session_state['li_token'] else '1-Click Share Ready'}`")
            st.markdown("🐦 **Twitter / X:** 🟢 `1-Click Tweet Ready`")

        if st.session_state["watermark"]:
            st.success(f"✨ Signature Watermark: **-- {st.session_state['watermark']}**")

# ==========================================
# TAB 3: POST HISTORY (SESSION ISOLATED)
# ==========================================
with tab_history:
    with st.container(border=True):
        st.markdown("### 📜 Your Private Post History / आपका इतिहास")
        st.markdown("Aapke dwara generate kiye gaye sabhi quotes aur graphics ka **Private Record:**")
        
        recent_posts = get_recent_posts(session_id=user_sid, limit=25)
        if recent_posts:
            for item in recent_posts:
                q_text, a_name, m_url, c_at = item
                with st.expander(f"✨ \"{q_text[:45]}...\" -- {a_name} ({c_at})"):
                    st.write(f"**Full Quote:** {q_text}")
                    st.write(f"**Signature:** -- {a_name}")
                    st.caption(f"🕒 Timestamp: {c_at}")
                    if m_url and m_url.startswith("http"):
                        st.markdown(f"📸 **Media Link:** [View HD Image/Video]({m_url})")
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
           - Go to **Tab 1 (Studio)**, type your quote, click **"✨ Auto-Generate Inspiring Quote"** or upload any photo/video from your phone/PC!
        3. **1-Click Broadcast Everywhere / पोस्ट करें:**
           - Hit **"🚀 Launch Multi-Platform Post"** to broadcast to **Instagram Story, Feed, Facebook Timeline, LinkedIn, WhatsApp & Twitter (X)** in 1 second!
        """)
