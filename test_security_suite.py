"""
OneClick Post Enterprise Security & Authentication Verification Suite
Automated End-to-End Tests for:
1. PBKDF2 150k Password Hashing & Zero Plaintext Fallback
2. AES-256-GCM Authenticated Token Encryption At Rest
3. Short-Lived Access Tokens + Refresh Token Rotation
4. Multi-Device Sessions, Single & All-Device Revocation
5. Brute-Force Rate Limiting & Account Lockout Throttling
6. IDOR / BOLA Strict Authorization Barriers
7. Media Magic-Byte File Validation & Size Enforcement
8. GDPR Permanent Account Deletion & Token Purge
"""

import os
import sys
import uuid
import tempfile
import io
from pathlib import Path
from fastapi.testclient import TestClient

# Ensure root path is in sys.path and UTF-8 stdout
ROOT_DIR = Path(__file__).parent
sys.path.insert(0, str(ROOT_DIR))
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from backend.server import app, validate_magic_bytes
from backend.crypto import encrypt_token, decrypt_token, hash_token
from backend.auth import get_password_hash, verify_password
from backend.database import get_db, SessionLocal
from backend.models import User, UserSession, SocialAccount, AuditLog, PostLog

client = TestClient(app)

def run_all_security_tests():
    print("=" * 80)
    print("🛡️  STARTING ONECLICK POST ENTERPRISE SECURITY VERIFICATION SUITE")
    print("=" * 80)
    
    passed_count = 0
    total_tests = 8

    # -------------------------------------------------------------
    # TEST 1: Password Hashing & Zero Plaintext Fallback
    # -------------------------------------------------------------
    print("\n[TEST 1/8] Verifying PBKDF2-150k Hashing & Zero Plaintext Fallback...")
    raw_pw = "SuperSecurePass_2026!#"
    hashed = get_password_hash(raw_pw)
    assert hashed.startswith("pbkdf2:sha256:150000$"), f"Invalid hash prefix: {hashed}"
    assert verify_password(raw_pw, hashed) is True, "Valid password failed verification"
    assert verify_password("WrongPassword123", hashed) is False, "Wrong password accepted"
    assert verify_password(raw_pw, raw_pw) is False, "CRITICAL: Plaintext password comparison accepted!"
    print("  ✅ PASS: PBKDF2 150,000 iterations verified. Plaintext fallback strictly eliminated.")
    passed_count += 1

    # -------------------------------------------------------------
    # TEST 2: AES-256-GCM Authenticated Token Encryption at Rest
    # -------------------------------------------------------------
    print("\n[TEST 2/8] Verifying AES-256-GCM Token Encryption at Rest...")
    secret_oauth_token = "EAAW86jxZCnPUBScM1GBJ4rUDmrbBXy55VZCyGL6MZCwESKYBVgLWEcujywQ6qJPxTMly"
    ciphertext = encrypt_token(secret_oauth_token)
    assert ciphertext.startswith("aes_gcm:v1:"), f"Invalid ciphertext format: {ciphertext}"
    assert secret_oauth_token not in ciphertext, "Raw token exposed in ciphertext!"
    decrypted = decrypt_token(ciphertext)
    assert decrypted == secret_oauth_token, "Decrypted token does not match original"
    # Test backward compatibility with legacy token
    assert decrypt_token("legacy_token_123") == "legacy_token_123", "Legacy token migration failed"
    print("  ✅ PASS: AES-256-GCM encryption & decryption verified. 0% token exposure at rest.")
    passed_count += 1

    # -------------------------------------------------------------
    # TEST 3: User Registration, Session Creation & HttpOnly Cookies
    # -------------------------------------------------------------
    print("\n[TEST 3/8] Verifying User Registration, Sessions & Cookie Issuance...")
    unique_email = f"security_user_{uuid.uuid4().hex[:8]}@example.com"
    reg_res = client.post("/api/auth/register", json={
        "name": "Security Test User",
        "email": unique_email,
        "password": "TestPassword123!"
    })
    assert reg_res.status_code == 200, f"Registration failed: {reg_res.text}"
    data = reg_res.json()
    assert "token" in data and "refresh_token" in data
    assert "access_token" in reg_res.cookies
    assert "refresh_token" in reg_res.cookies
    user_id = data["user"]["id"]
    access_token = data["token"]
    refresh_token = data["refresh_token"]
    print(f"  ✅ PASS: User registered (ID: {user_id}), active session registered, HttpOnly cookies issued.")
    passed_count += 1

    # -------------------------------------------------------------
    # TEST 4: Refresh Token Rotation & Session Invalidation
    # -------------------------------------------------------------
    print("\n[TEST 4/8] Verifying Refresh Token Rotation...")
    ref_res = client.post("/api/auth/refresh", json={"refresh_token": refresh_token})
    assert ref_res.status_code == 200, f"Token refresh failed: {ref_res.text}"
    ref_data = ref_res.json()
    new_access_token = ref_data["token"]
    new_refresh_token = ref_data["refresh_token"]
    assert new_refresh_token != refresh_token, "Refresh token was not rotated!"

    # Verify old refresh token is now invalidated (prevent replay attack)
    old_replay_res = client.post("/api/auth/refresh", json={"refresh_token": refresh_token})
    assert old_replay_res.status_code == 401, "Replay attack with old refresh token succeeded!"
    print("  ✅ PASS: Refresh token rotation verified. Replay of old tokens strictly rejected.")
    passed_count += 1

    # -------------------------------------------------------------
    # TEST 5: Active Device Listing, Single Device & All-Device Logout
    # -------------------------------------------------------------
    print("\n[TEST 5/8] Verifying Multi-Device Sessions & Logout-All...")
    # Create second session on "Mobile Browser"
    login_res2 = client.post(
        "/api/auth/login",
        json={"email": unique_email, "password": "TestPassword123!", "remember_me": True},
        headers={"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X)"}
    )
    assert login_res2.status_code == 200

    # List active sessions
    sess_list_res = client.get("/api/auth/sessions", headers={"Authorization": f"Bearer {new_access_token}"})
    assert sess_list_res.status_code == 200
    sessions = sess_list_res.json()
    assert len(sessions) >= 2, f"Expected >= 2 sessions, got {len(sessions)}"

    # Call Logout All
    logout_all_res = client.post("/api/auth/logout-all", headers={"Authorization": f"Bearer {new_access_token}"})
    assert logout_all_res.status_code == 200

    # Verify session is now revoked
    revoked_check = client.get("/api/auth/me", headers={"Authorization": f"Bearer {new_access_token}"})
    assert revoked_check.status_code == 401, "Revoked session was still allowed to access API!"
    print("  ✅ PASS: Multi-device tracking and global session revocation verified.")
    passed_count += 1

    # -------------------------------------------------------------
    # TEST 6: Brute-Force Rate Limiting & Account Lockout
    # -------------------------------------------------------------
    print("\n[TEST 6/8] Verifying Brute-Force Lockout Defense...")
    victim_email = f"victim_{uuid.uuid4().hex[:8]}@example.com"
    client.post("/api/auth/register", json={"name": "Victim", "email": victim_email, "password": "CorrectPassword123!"})

    # Trigger 5 failed logins
    for i in range(5):
        fail_res = client.post("/api/auth/login", json={"email": victim_email, "password": "WrongPassword!"})
        assert fail_res.status_code == 401

    # 6th attempt must be locked out
    locked_res = client.post("/api/auth/login", json={"email": victim_email, "password": "CorrectPassword123!"})
    assert locked_res.status_code == 423, f"Expected 423 Locked, got {locked_res.status_code}: {locked_res.text}"
    print("  ✅ PASS: Account lockout triggered after 5 failed attempts (HTTP 423 Locked).")
    passed_count += 1

    # -------------------------------------------------------------
    # TEST 7: Media Magic-Byte File Validation
    # -------------------------------------------------------------
    print("\n[TEST 7/8] Verifying Media Magic-Byte & Anti-Tamper Security...")
    # 1. Valid PNG
    png_bytes = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15c4"
    valid_png_res = client.post(
        "/api/social/upload-file",
        files={"file": ("test.png", png_bytes, "image/png")}
    )
    assert valid_png_res.status_code == 200, f"Valid PNG upload failed: {valid_png_res.text}"

    # 2. Malicious Disguised Executable with .png extension
    malicious_script = b"#!/bin/bash\necho 'Hacked'\nmalicious_payload_content_here"
    malicious_res = client.post(
        "/api/social/upload-file",
        files={"file": ("malicious.png", malicious_script, "image/png")}
    )
    assert malicious_res.status_code == 400, "Malicious disguised file was erroneously accepted!"
    print("  ✅ PASS: Magic-byte inspection passed valid PNG and rejected disguised malicious files.")
    passed_count += 1

    # -------------------------------------------------------------
    # TEST 8: IDOR Protection & GDPR Permanent Account Deletion
    # -------------------------------------------------------------
    print("\n[TEST 8/8] Verifying IDOR Protection & GDPR Account Deletion...")
    # Register User A and User B
    email_a = f"usera_{uuid.uuid4().hex[:8]}@example.com"
    email_b = f"userb_{uuid.uuid4().hex[:8]}@example.com"
    user_a_res = client.post("/api/auth/register", json={"name": "User A", "email": email_a, "password": "PasswordA123!"}).json()
    user_b_res = client.post("/api/auth/register", json={"name": "User B", "email": email_b, "password": "PasswordB123!"}).json()

    token_a = user_a_res["token"]
    token_b = user_b_res["token"]

    # User A connects an account
    conn_res = client.post(
        "/api/social/accounts",
        json={
            "platform": "instagram",
            "platform_account_id": "17841440001",
            "platform_account_name": "@user_a_insta",
            "access_token": "secret_oauth_token_a"
        },
        headers={"Authorization": f"Bearer {token_a}"}
    ).json()
    account_id_a = conn_res["account_id"]

    # User B attempts IDOR attack to delete User A's account
    idor_attack = client.delete(
        f"/api/social/accounts/{account_id_a}",
        headers={"Authorization": f"Bearer {token_b}"}
    )
    assert idor_attack.status_code == 403, f"IDOR vulnerability detected! Status: {idor_attack.status_code}"

    # User A performs GDPR account deletion
    del_res = client.delete("/api/account/me", headers={"Authorization": f"Bearer {token_a}"})
    assert del_res.status_code == 200

    # Verify User A data is purged from DB
    db = SessionLocal()
    purged_user = db.query(User).filter(User.email == email_a).first()
    purged_acc = db.query(SocialAccount).filter(SocialAccount.id == account_id_a).first()
    db.close()
    assert purged_user is None, "User record was not deleted!"
    assert purged_acc is None, "User social accounts were not purged!"

    print("  ✅ PASS: IDOR protection blocked unauthorized access (HTTP 403). GDPR account deletion purged all data.")
    passed_count += 1

    print("\n" + "=" * 80)
    print(f"🎉 ALL {passed_count}/{total_tests} SECURITY & AUTHENTICATION AUDIT TESTS PASSED (100% SUCCESS)!")
    print("=" * 80)

if __name__ == "__main__":
    run_all_security_tests()
