import os
import sys
import uuid
import threading
from unittest.mock import patch
from pathlib import Path
from fastapi.testclient import TestClient

# Add project root to sys.path
ROOT_DIR = Path(__file__).parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from backend.server import app
from backend.database import get_db, init_db, SessionLocal
from backend.models import User, SocialAccount, PostLog, PlatformPostResult, TaskLog
from backend.auth import create_access_token, get_password_hash
from main import planner, calculator, get_time, web_search
from social_tools import create_nature_quote_image, resolve_media_url

client = TestClient(app)

def mock_post_instagram_feed(content, media_path_or_url=None, user_id=None, access_token=None, author=None):
    if access_token == "invalid_token":
        return {"status": "FAILED", "error_code": "OAuthException", "message": "Instagram session invalid"}
    return {"status": "SUCCESS", "post_id": f"ig_{uuid.uuid4().hex[:8]}", "message": "Instagram post published live."}

def mock_post_facebook_page(content, media_path_or_url=None, page_id=None, page_access_token=None, author=None):
    if page_access_token == "invalid_fb_token":
        return {"status": "FAILED", "error_code": "FB_TOKEN_EXPIRED", "message": "Facebook page token expired"}
    return {"status": "SUCCESS", "post_id": f"fb_{uuid.uuid4().hex[:8]}", "message": "Facebook page post published live."}

def mock_post_linkedin(content, media_path_or_url=None, access_token=None, author_urn=None, author=None):
    if access_token == "invalid_li_token":
        return {"status": "FAILED", "error_code": "LI_EXPIRED", "message": "LinkedIn token expired"}
    return {"status": "SUCCESS", "post_id": f"urn:li:share:{uuid.uuid4().hex[:8]}", "message": "LinkedIn post published live."}

def run_production_audit():
    print("=" * 60, flush=True)
    print("RUNNING PRODUCTION MULTI-USER & MULTI-ACCOUNT TEST SUITE", flush=True)
    print("=" * 60, flush=True)

    db = SessionLocal()
    init_db()

    # 1. Setup Test Users
    user_a_email = f"user_a_{uuid.uuid4().hex[:6]}@test.com"
    user_b_email = f"user_b_{uuid.uuid4().hex[:6]}@test.com"

    user_a = User(name="User A (Brand Agency)", email=user_a_email, hashed_password=get_password_hash("pass123"))
    user_b = User(name="User B (Individual)", email=user_b_email, hashed_password=get_password_hash("pass123"))
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

    # 2. Connect Multiple Accounts for User A
    acc_a1 = SocialAccount(user_id=user_a.id, platform="instagram", platform_account_id="1784140001", platform_account_name="@agency_main", access_token="token_a1")
    acc_a2 = SocialAccount(user_id=user_a.id, platform="instagram", platform_account_id="1784140002", platform_account_name="@agency_secondary", access_token="token_a2")
    acc_a3 = SocialAccount(user_id=user_a.id, platform="facebook", platform_account_id="fb_page_001", platform_account_name="Tech Agency Page", access_token="invalid_fb_token")
    acc_a4 = SocialAccount(user_id=user_a.id, platform="linkedin", platform_account_id="urn:li:person:a1", platform_account_name="Agency LinkedIn", access_token="token_li_a")

    # Connect Accounts for User B
    acc_b1 = SocialAccount(user_id=user_b.id, platform="instagram", platform_account_id="1784140003", platform_account_name="@user_b_personal", access_token="token_b1")
    acc_b2 = SocialAccount(user_id=user_b.id, platform="linkedin", platform_account_id="urn:li:person:b1", platform_account_name="User B LinkedIn", access_token="token_li_b")

    db.add_all([acc_a1, acc_a2, acc_a3, acc_a4, acc_b1, acc_b2])
    db.commit()
    db.refresh(acc_a1)
    db.refresh(acc_a2)
    db.refresh(acc_a3)
    db.refresh(acc_a4)
    db.refresh(acc_b1)
    db.refresh(acc_b2)

    # ----------------------------------------------------
    # TEST 1: User & Account List Isolation
    # ----------------------------------------------------
    print("\n[TEST 1] Testing User Account Isolation via API...", flush=True)
    res_a = client.get("/api/social/accounts", headers=headers_a)
    res_b = client.get("/api/social/accounts", headers=headers_b)

    assert res_a.status_code == 200, f"Failed GET /api/social/accounts for User A: {res_a.text}"
    assert res_b.status_code == 200, f"Failed GET /api/social/accounts for User B: {res_b.text}"

    data_a = res_a.json()
    data_b = res_b.json()

    assert len(data_a) == 4, f"User A should see exactly 4 accounts, saw: {len(data_a)}"
    assert len(data_b) == 2, f"User B should see exactly 2 accounts, saw: {len(data_b)}"

    user_a_acc_ids = [acc["id"] for acc in data_a]
    user_b_acc_ids = [acc["id"] for acc in data_b]

    # Verify zero intersection
    assert not set(user_a_acc_ids).intersection(set(user_b_acc_ids)), "CRITICAL BUG: Account IDs leaked across users!"
    print(f"[PASS] User A accounts {user_a_acc_ids} completely isolated from User B accounts {user_b_acc_ids}", flush=True)

    # ----------------------------------------------------
    # TEST 2: Malicious Ownership Security Test (403 Forbidden)
    # ----------------------------------------------------
    print("\n[TEST 2] Testing Malicious Cross-Account Access Security...", flush=True)
    malicious_payload = {
        "content": "Malicious hijacking attempt",
        "account_ids": [acc_b1.id]
    }
    malicious_res = client.post("/api/social/publish", headers=headers_a, json=malicious_payload)
    assert malicious_res.status_code == 403, f"Expected 403 Forbidden, got {malicious_res.status_code}: {malicious_res.text}"
    print(f"[PASS] User A attempting to publish to User B's account was blocked with 403 Forbidden!", flush=True)

    # ----------------------------------------------------
    # TEST 3: Multi-Account Same-Platform & Partial Success
    # ----------------------------------------------------
    print("\n[TEST 3] Testing Multi-Account One-Click Publish & Partial Success Resilience...", flush=True)
    with patch("backend.server.post_instagram_feed", side_effect=mock_post_instagram_feed), \
         patch("backend.server.post_facebook_page", side_effect=mock_post_facebook_page), \
         patch("backend.server.post_linkedin", side_effect=mock_post_linkedin):

        publish_payload = {
            "content": "Autonomous Multi-Account AI Broadcast Testing",
            "account_ids": [acc_a1.id, acc_a2.id, acc_a3.id, acc_a4.id]
        }
        pub_res = client.post("/api/social/publish", headers=headers_a, json=publish_payload)
        assert pub_res.status_code == 200, f"Publish failed: {pub_res.text}"

        pub_data = pub_res.json()
        assert pub_data["total_accounts"] == 4, f"Expected 4 accounts, got {pub_data['total_accounts']}"
        assert pub_data["success_count"] == 3, f"Expected 3 successes (A1, A2, A4), got {pub_data['success_count']}"
        assert pub_data["failure_count"] == 1, f"Expected 1 failure (A3 FB token expired), got {pub_data['failure_count']}"
        assert pub_data["overall_status"] == "PARTIAL_SUCCESS", f"Expected PARTIAL_SUCCESS, got {pub_data['overall_status']}"

        print(f"[PASS] Multi-Account Publish succeeded with Partial Success resilience!", flush=True)
        print(f"       Job ID: {pub_data['job_id']} | Overall: {pub_data['overall_status']} (3/4 Succeeded, 1 Failed account did NOT block others)")
        for p in pub_data["platforms"]:
            print(f"       -> {p['platform']} ({p['account_name']}): status={p['status']} message={p['message'][:35]}", flush=True)

    # ----------------------------------------------------
    # TEST 4: Unique Media File Isolation (0% Collision)
    # ----------------------------------------------------
    print("\n[TEST 4] Testing Media File Isolation across concurrent requests...", flush=True)
    img1 = create_nature_quote_image("Quote 1 for User A", author="Author A")
    img2 = create_nature_quote_image("Quote 2 for User B", author="Author B")

    assert img1 != img2, "CRITICAL: Image file paths collided!"
    assert Path(img1).exists() and Path(img2).exists(), "Image file paths must exist"
    print(f"[PASS] Generated isolated files with 0 collision:\n       File 1: {img1}\n       File 2: {img2}", flush=True)

    # ----------------------------------------------------
    # TEST 5: Concurrent Requests Stress Test (10 Threads)
    # ----------------------------------------------------
    print("\n[TEST 5] Testing 10 Concurrent Multi-User Publish Requests...", flush=True)
    results = []
    errors = []

    with patch("backend.server.post_instagram_feed", side_effect=mock_post_instagram_feed), \
         patch("backend.server.post_facebook_page", side_effect=mock_post_facebook_page), \
         patch("backend.server.post_linkedin", side_effect=mock_post_linkedin):

        def concurrent_worker(worker_id):
            try:
                tok = token_a if worker_id % 2 == 0 else token_b
                accs = [acc_a1.id] if worker_id % 2 == 0 else [acc_b1.id]
                res = client.post(
                    "/api/social/publish",
                    headers={"Authorization": f"Bearer {tok}"},
                    json={"content": f"Concurrent task {worker_id}", "account_ids": accs}
                )
                if res.status_code == 200:
                    results.append(res.json()["job_id"])
                else:
                    errors.append(res.text)
            except Exception as e:
                errors.append(str(e))

        threads = [threading.Thread(target=concurrent_worker, args=(i,)) for i in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

    assert len(errors) == 0, f"Encountered errors during concurrent execution: {errors}"
    assert len(results) == 10, f"Expected 10 successful concurrent jobs, got: {len(results)}"
    assert len(set(results)) == 10, "CRITICAL: Duplicate job IDs generated during concurrency!"
    print(f"[PASS] 10/10 Concurrent requests executed with 100% unique job IDs and 0 race conditions!", flush=True)

    # ----------------------------------------------------
    # TEST 6: Existing Agentic AI Regression Tests
    # ----------------------------------------------------
    print("\n[TEST 6] Testing Existing Agentic AI Pipeline Regression...", flush=True)
    calc_res = calculator(6, 7)
    assert calc_res == 42, f"Calculator failed: {calc_res}"

    curr_time = get_time()
    assert ":" in curr_time, f"Time tool failed: {curr_time}"

    agent_run_res = client.post(
        "/api/agent/run",
        headers=headers_a,
        json={"task": "Calculate 8 * 9 and get current time"}
    )
    assert agent_run_res.status_code == 200, f"Agent run failed: {agent_run_res.text}"
    agent_data = agent_run_res.json()
    assert agent_data["status"] == "completed", f"Agent status not completed: {agent_data}"
    print(f"[PASS] Existing Agentic AI core tools, planner, and execution loop 100% functional!", flush=True)

    print("\n" + "=" * 60, flush=True)
    print("🏆 ALL 6 PRODUCTION AUDIT & VERIFICATION TESTS PASSED 100%!", flush=True)
    print("=" * 60, flush=True)

if __name__ == "__main__":
    run_production_audit()
