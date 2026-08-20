import os
import sys
import uuid
import threading
from unittest.mock import patch, MagicMock
from pathlib import Path
from fastapi.testclient import TestClient
from jose import jwt

# Add project root to sys.path
ROOT_DIR = Path(__file__).parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from backend.server import app, SECRET_KEY, ALGORITHM
from backend.database import get_db, init_db, SessionLocal
from backend.models import User, SocialAccount, PostLog, PlatformPostResult, TaskLog
from backend.auth import create_access_token, get_password_hash
from main import planner, calculator, get_time, web_search

client = TestClient(app)

def run_oauth_and_publishing_tests():
    print("=" * 65, flush=True)
    print("🚀 RUNNING META OAUTH, MULTI-ACCOUNT & USER ISOLATION TEST SUITE", flush=True)
    print("=" * 65, flush=True)

    db = SessionLocal()
    init_db()

    # 1. Create Isolated Users
    user_a_email = f"agency_user_{uuid.uuid4().hex[:6]}@domain.com"
    user_b_email = f"individual_user_{uuid.uuid4().hex[:6]}@domain.com"

    user_a = User(name="Agency Admin", email=user_a_email, hashed_password=get_password_hash("pass123"))
    user_b = User(name="Personal Creator", email=user_b_email, hashed_password=get_password_hash("pass123"))
    db.add(user_a)
    db.add(user_b)
    db.commit()
    db.refresh(user_a)
    db.refresh(user_b)

    token_a = create_access_token({"sub": user_a.email, "id": user_a.id, "name": user_a.name})
    token_b = create_access_token({"sub": user_b.email, "id": user_b.id, "name": user_b.name})

    headers_a = {"Authorization": f"Bearer {token_a}"}
    headers_b = {"Authorization": f"Bearer {token_b}"}

    print(f"[OK] Created isolated users: User A (ID: {user_a.id}), User B (ID: {user_b.id})", flush=True)

    # ----------------------------------------------------
    # TEST 1: Meta OAuth URL Generation with Signed State
    # ----------------------------------------------------
    print("\n[TEST 1] Testing Meta OAuth Authorization URL Generation...", flush=True)
    url_res = client.get("/api/auth/meta/url", headers=headers_a)
    assert url_res.status_code == 200, f"Failed GET /api/auth/meta/url: {url_res.text}"
    url_data = url_res.json()
    auth_url = url_data.get("auth_url", "")
    assert "https://www.facebook.com/v21.0/dialog/oauth" in auth_url, f"Invalid OAuth URL: {auth_url}"
    assert "state=" in auth_url, "Missing signed state parameter in OAuth URL"

    # Extract state and verify signature
    state_token = auth_url.split("state=")[1].split("&")[0]
    payload = jwt.decode(state_token, SECRET_KEY, algorithms=[ALGORITHM])
    assert payload.get("user_id") == user_a.id, f"State user_id {payload.get('user_id')} does not match User A {user_a.id}"
    print(f"[PASS] Meta OAuth URL successfully generated with secure signed user_id state.", flush=True)

    # ----------------------------------------------------
    # TEST 2: Tampered State Security Rejection
    # ----------------------------------------------------
    print("\n[TEST 2] Testing Tampered State Security in OAuth Callback...", flush=True)
    tampered_res = client.get("/api/auth/meta/callback?code=mock_code&state=invalid_tampered_state", follow_redirects=False)
    assert tampered_res.status_code == 307 or tampered_res.status_code == 200, "Should redirect on error"
    redirect_loc = tampered_res.headers.get("location", "")
    assert "oauth=error" in redirect_loc, f"Expected error redirect, got: {redirect_loc}"
    print(f"[PASS] Tampered OAuth state token properly rejected and redirected to error.", flush=True)

    # ----------------------------------------------------
    # TEST 3: Meta OAuth Callback Multi-Account Discovery
    # ----------------------------------------------------
    print("\n[TEST 3] Testing Meta OAuth Callback Account Discovery & Token Storage...", flush=True)
    
    mock_token_resp = MagicMock()
    mock_token_resp.status_code = 200
    mock_token_resp.json.return_value = {"access_token": "mock_short_user_token"}

    mock_exchange_resp = MagicMock()
    mock_exchange_resp.status_code = 200
    mock_exchange_resp.json.return_value = {"access_token": "mock_60_day_long_token"}

    mock_accounts_resp = MagicMock()
    mock_accounts_resp.status_code = 200
    mock_accounts_resp.json.return_value = {
        "data": [
            {
                "id": "1001",
                "name": "Agency Main Page",
                "access_token": "page_token_1001",
                "instagram_business_account": {
                    "id": "178414999901",
                    "username": "agency_brand_main"
                }
            },
            {
                "id": "1002",
                "name": "Agency Secondary Page",
                "access_token": "page_token_1002",
                "instagram_business_account": {
                    "id": "178414999902",
                    "username": "agency_brand_secondary"
                }
            }
        ]
    }

    def mock_get(url, params=None, **kwargs):
        if "oauth/access_token" in url and params and params.get("grant_type") == "fb_exchange_token":
            return mock_exchange_resp
        elif "oauth/access_token" in url:
            return mock_token_resp
        elif "me/accounts" in url:
            return mock_accounts_resp
        return MagicMock(status_code=404)

    with patch("httpx.Client.get", side_effect=mock_get):
        cb_res = client.get(f"/api/auth/meta/callback?code=valid_code&state={state_token}", follow_redirects=False)
        assert cb_res.status_code == 307 or cb_res.status_code == 200
        assert "oauth=success" in cb_res.headers.get("location", "")

    # Verify accounts were added for User A
    accounts_a = db.query(SocialAccount).filter(SocialAccount.user_id == user_a.id).all()
    ig_names = [a.platform_account_name for a in accounts_a if a.platform == "instagram"]
    fb_names = [a.platform_account_name for a in accounts_a if a.platform == "facebook"]

    assert "@agency_brand_main" in ig_names, f"Missing @agency_brand_main in {ig_names}"
    assert "@agency_brand_secondary" in ig_names, f"Missing @agency_brand_secondary in {ig_names}"
    assert len(accounts_a) == 4, f"Expected 4 accounts (2 IG + 2 FB Pages), got {len(accounts_a)}"
    print(f"[PASS] Meta OAuth Callback discovered and saved: {ig_names} & {fb_names}", flush=True)

    # ----------------------------------------------------
    # TEST 4: Token Non-Exposure in API Responses
    # ----------------------------------------------------
    print("\n[TEST 4] Testing Safe API Responses (Zero Token Exposure)...", flush=True)
    list_res = client.get("/api/social/accounts", headers=headers_a)
    assert list_res.status_code == 200
    for acc_item in list_res.json():
        assert "access_token" not in acc_item, f"SECURITY LEAK: access_token found in {acc_item}"
        assert "refresh_token" not in acc_item, f"SECURITY LEAK: refresh_token found in {acc_item}"
    print(f"[PASS] GET /api/social/accounts returns safe metadata with 0 token leakage.", flush=True)

    # ----------------------------------------------------
    # TEST 5: User Isolation (User B cannot see User A's accounts)
    # ----------------------------------------------------
    print("\n[TEST 5] Testing Multi-User Account Isolation...", flush=True)
    list_b = client.get("/api/social/accounts", headers=headers_b)
    assert list_b.status_code == 200
    assert len(list_b.json()) == 0, f"User B should have 0 accounts, saw: {list_b.json()}"
    print(f"[PASS] User B cannot see any of User A's accounts.", flush=True)

    # ----------------------------------------------------
    # TEST 6: One-Click Multi-Account Publishing & Partial Success
    # ----------------------------------------------------
    print("\n[TEST 6] Testing One-Click Publishing to Multiple Instagram Accounts...", flush=True)
    user_a_acc_ids = [a.id for a in accounts_a]

    def mock_post_ig(content, media_path_or_url=None, user_id=None, access_token=None, author=None):
        if user_id == "178414999902":
            return {"status": "FAILED", "error_code": "AUTH_EXPIRED", "message": "Instagram token expired. Please reconnect."}
        return {"status": "SUCCESS", "post_id": f"ig_{uuid.uuid4().hex[:8]}", "message": "Instagram post published live."}

    def mock_post_fb(content, media_path_or_url=None, page_id=None, page_access_token=None, author=None):
        return {"status": "SUCCESS", "post_id": f"fb_{uuid.uuid4().hex[:8]}", "message": "Facebook page post published live."}

    with patch("backend.server.post_instagram_feed", side_effect=mock_post_ig), \
         patch("backend.server.post_facebook_page", side_effect=mock_post_fb):

        publish_payload = {
            "content": "Aesthetic Nature Motivation Post",
            "account_ids": user_a_acc_ids
        }
        pub_res = client.post("/api/social/publish", headers=headers_a, json=publish_payload)
        assert pub_res.status_code == 200
        pub_data = pub_res.json()

        assert pub_data["total_accounts"] == 4
        assert pub_data["success_count"] == 3
        assert pub_data["failure_count"] == 1
        assert pub_data["overall_status"] == "PARTIAL_SUCCESS"

        print(f"[PASS] 1-Click Multi-Account Publish succeeded! Overall Status: {pub_data['overall_status']}", flush=True)
        for p in pub_data["platforms"]:
            print(f"       -> {p['platform']} ({p['account_name']}): status={p['status']} message={p['message'][:35]}", flush=True)

    # ----------------------------------------------------
    # TEST 7: Existing Agentic AI Regression Tests
    # ----------------------------------------------------
    print("\n[TEST 7] Testing Existing Agentic AI Pipeline Compatibility...", flush=True)
    assert calculator(12, 12) == 144
    assert ":" in get_time()
    
    agent_res = client.post("/api/agent/run", headers=headers_a, json={"task": "Calculate 9 * 9 and get current time"})
    assert agent_res.status_code == 200
    assert agent_res.json()["status"] == "completed"
    print(f"[PASS] Existing Agentic AI core tools and execution loop 100% functional!", flush=True)

    print("\n" + "=" * 65, flush=True)
    print("🏆 ALL 7 META OAUTH & MULTI-USER ISOLATION TESTS PASSED 100%!", flush=True)
    print("=" * 65, flush=True)

if __name__ == "__main__":
    run_oauth_and_publishing_tests()
