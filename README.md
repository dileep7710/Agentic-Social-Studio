# 🌌 Agentic AI Multi-Platform Social Studio

An autonomous, multi-platform AI-powered social media publishing suite built in Python and Streamlit. Publish 4K neural graphics, custom photos, and videos to **Instagram, Facebook, LinkedIn, and WhatsApp** simultaneously in 1-Click.

---

## 🌟 Key Features

- 📸 **Instagram Pro Suite:** Publish 24-hour Stories, permanent Feed posts, and Video Reels via Meta Graph API.
- 📘 **Facebook Direct Timeline:** Direct timeline photo and text dispatch.
- 💼 **LinkedIn Professional:** One-click publishing to LinkedIn feed via official LinkedIn REST API.
- 💬 **WhatsApp Engine:** Silent background delivery of high-res graphics and captions.
- ✨ **4K Neural Graphic Generator:** Auto-generates aesthetic quotes and 4K wallpapers using local Llama 3.2 3B AI.
- 📂 **Local PC Folder Uploader:** Drag-and-drop or select any `.png`, `.jpg`, or `.mp4` from your local computer.
- 🌐 **Bilingual Interface:** Toggle between **English** and **हिन्दी (Hindi)** with one click.
- 🛡️ **100% Private & Secure:** Zero cloud logging. All session tokens and credentials remain isolated on the user's device.

---

## 🚀 Quick Start (Local Setup)

### 1. Clone the Repository
```bash
git clone https://github.com/dileep7710/Agentic-Social-Studio.git
cd Agentic-Social-Studio
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
playwright install chromium
```

### 3. Configure Environment Variables
Copy `.env.example` to `.env` and enter your API keys:
```bash
cp .env.example .env
```

### 4. Launch the Web Studio
Double-click `Launch_AI_Studio.bat` or run in terminal:
```bash
streamlit run app.py
```
Open `http://localhost:8501` in your browser.

---

## ☁️ 1-Click Cloud Deployment (Streamlit Community Cloud)

1. Fork or push this repository to your GitHub account.
2. Visit [share.streamlit.io](https://share.streamlit.io).
3. Select this repository: `Agentic-Social-Studio`, branch `main`, and main file `app.py`.
4. Click **Deploy!**

---

## 🛡️ License & Privacy
This project is open-source under the MIT License. No personal data or private credentials are stored in this repository.
