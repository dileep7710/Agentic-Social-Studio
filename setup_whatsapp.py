import time
from pathlib import Path
from playwright.sync_api import sync_playwright

session_dir = Path(r"c:\Users\Dileep Yadav\Desktop\AgenticAI\whatsapp_session")
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"

print("==================================================")
print("      WHATSAPP 1-TIME QR SCAN SETUP (45 SECONDS)")
print("==================================================")
print("Opening browser window on your screen...")

with sync_playwright() as p:
    context = p.chromium.launch_persistent_context(
        user_data_dir=str(session_dir),
        headless=False,
        user_agent=USER_AGENT,
        viewport={"width": 1280, "height": 800},
        args=["--no-sandbox", "--disable-blink-features=AutomationControlled"]
    )
    page = context.pages[0] if context.pages else context.new_page()
    page.goto("https://web.whatsapp.com", timeout=60000)
    
    print("\n👉 Please SCAN the QR code on your screen using your WhatsApp mobile app now!")
    print("Waiting 45 seconds to let you scan and sync...")
    
    for i in range(45, 0, -1):
        print(f"Time remaining: {i}s...", end="\r")
        time.sleep(1)
        
    print("\n✅ WhatsApp Session saved permanently in 'whatsapp_session' folder!")
    context.close()
