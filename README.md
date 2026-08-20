# 🌌 Agentic AI Omni-Studio (Full-Stack Edition)

> **Autonomous AI Assistant for Web Research & 1-Click Multi-Platform Broadcasting**  
> Powered by Llama 3.2, Python FastAPI, React 18, Vite, Tailwind CSS, and SQLite.

---

## 🌟 Architectural Overview

```
                                  ┌────────────────────────────────┐
                                  │   React + Vite + Tailwind UI   │
                                  │ (Landing, Assistant, Social)   │
                                  └───────────────┬────────────────┘
                                                  │ Axios / REST API
                                                  ▼
                                  ┌────────────────────────────────┐
                                  │     FastAPI Backend Router     │
                                  │  (JWT Auth, Tasks, Proxy)      │
                                  └───────────────┬────────────────┘
                                                  │ Calls directly
                                                  ▼
                                  ┌────────────────────────────────┐
                                  │      Existing Agent Engine     │
                                  │  (main.py / planner / tools)   │
                                  └───────────────┬────────────────┘
                                                  │
                          ┌───────────────────────┴───────────────────────┐
                          ▼                                               ▼
              ┌───────────────────────┐                       ┌───────────────────────┐
              │    Existing Tools     │                       │    Database Storage   │
              │ (Search, Calc, Social)│                       │  (Users, Tasks, Hist) │
              └───────────────────────┘                       └───────────────────────┘
```

---

## 🚀 Key Features

1. **Autonomous Task Planner (`planner` in `main.py`)**:
   - Decomposes complex user goals into 2–5 structured action steps.
2. **Live Internet Web Research (`web_search` with DDGS)**:
   - Queries duckduckgo in real-time, extracts verified sources with citations and summaries.
3. **1-Click Multi-Platform Social Broadcast (`social_tools.py`)**:
   - Generates 4K aesthetic quote graphics with customizable watermark signatures.
   - 1-Click sharing across **Instagram (Story/Feed), Facebook Timeline, LinkedIn, and WhatsApp**.
4. **Persistent Conversational Memory (`memory.json`)**:
   - Remembers past context across multiple sessions.
5. **JWT Authentication & Task Audit Logs (`SQLite + SQLAlchemy`)**:
   - Secure user authentication with password hashing and searchable task history tables.

---

## 🛠️ How to Run the Project Locally

### Option 1: One-Click Launcher (Windows)
Double-click:
```
Launch_FullStack_SaaS.bat
```
This automatically boots the FastAPI backend and opens `http://127.0.0.1:8000` in your default browser.

---

### Option 2: Running Terminal CLI Agent (Classic Mode)
You can still use the original CLI agent at any time without any change:
```bash
.\venv\Scripts\python.exe main.py
```

---

### Option 3: Running Backend & Frontend in Development Mode

#### 1. Start FastAPI Backend Server:
```bash
.\venv\Scripts\uvicorn.exe backend.server:app --host 127.0.0.1 --port 8000 --reload
```
- **Backend API:** `http://127.0.0.1:8000`
- **Interactive Swagger Docs:** `http://127.0.0.1:8000/docs`

#### 2. Start React + Vite Frontend (Dev Server):
```bash
cd frontend
npm run dev
```
- **Frontend Dev URL:** `http://localhost:5173`

---

## 📁 Directory Structure

```
AgenticAI/
├── backend/
│   ├── agent_bridge.py      # Bridge wrapping main.py & social_tools.py
│   ├── auth.py              # JWT authentication & bcrypt password hashing
│   ├── database.py          # SQLite database connection & sessions
│   ├── models.py            # SQLAlchemy models (User, TaskLog, PlatformSettings)
│   └── server.py            # FastAPI main application & API routes
│
├── frontend/
│   ├── src/
│   │   ├── components/      # Navbar, Sidebar, AgentExecutionUI
│   │   ├── context/         # AuthContext with JWT management
│   │   ├── pages/           # Landing, Dashboard, Social, History, Settings, Auth
│   │   ├── App.jsx          # React Router setup
│   │   └── main.jsx         # React DOM mount point
│   ├── package.json
│   ├── tailwind.config.js
│   └── vite.config.js
│
├── main.py                  # Original CLI Agentic AI (100% Preserved)
├── social_tools.py          # 4K Nature image generator & social posting tools
├── memory.json              # Conversational memory buffer
├── requirements.txt         # Backend Python dependencies
├── Launch_FullStack_SaaS.bat# Windows one-click SaaS launcher
└── README.md
```

---

## 📡 API Endpoints Documentation

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/auth/register` | Register new user account |
| `POST` | `/api/auth/login` | Login user & retrieve JWT bearer token |
| `GET` | `/api/auth/me` | Retrieve authenticated user profile |
| `POST` | `/api/agent/run` | Execute goal with planner, tools & web search |
| `GET` | `/api/tasks` | Retrieve user task history & audit logs |
| `GET` | `/api/tasks/{id}` | Retrieve specific task execution trace |
| `GET` | `/api/social/status` | Retrieve connection states for all platforms |
| `POST` | `/api/social/publish`| 1-Click 4K graphic generator & CDN broadcast |
| `GET` | `/api/settings` | Retrieve user watermark & WhatsApp branding |
| `POST` | `/api/settings` | Update user watermark & settings in SQLite |
