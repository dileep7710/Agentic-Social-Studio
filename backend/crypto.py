"""
Cryptographic Engine for OneClick Post
Implements AES-256-GCM Authenticated Encryption for OAuth tokens at rest,
key derivation, and SHA-256 secure token hashing.
"""

import os
import hashlib
import secrets
from typing import Optional
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from dotenv import load_dotenv

load_dotenv()

# Master 256-bit Encryption Key for OAuth tokens at rest
_RAW_KEY = os.getenv("ENCRYPTION_KEY", "")
if not _RAW_KEY:
    # Deterministic fallback for dev if not explicitly defined
    _RAW_KEY = os.getenv("JWT_SECRET", "agentic_ai_omni_studio_master_encryption_key_2026")

# Derive fixed 32-byte (256-bit) AES key using SHA-256
AES_KEY_BYTES = hashlib.sha256(_RAW_KEY.encode("utf-8")).digest()
_aesgcm = AESGCM(AES_KEY_BYTES)


def encrypt_token(plaintext: Optional[str]) -> Optional[str]:
    """
    Encrypts sensitive OAuth access_token or refresh_token using AES-256-GCM.
    Output format: aes_gcm:v1:<nonce_hex>:<ciphertext_and_tag_hex>
    """
    if not plaintext:
        return None
    
    # Generate 12-byte (96-bit) unique nonce for GCM
    nonce = secrets.token_bytes(12)
    ciphertext = _aesgcm.encrypt(nonce, plaintext.encode("utf-8"), None)
    return f"aes_gcm:v1:{nonce.hex()}:{ciphertext.hex()}"


def decrypt_token(ciphertext: Optional[str]) -> Optional[str]:
    """
    Decrypts an AES-256-GCM encrypted token.
    Gracefully returns plaintext if the input is legacy unencrypted data.
    """
    if not ciphertext:
        return ""
    
    if not ciphertext.startswith("aes_gcm:v1:"):
        # Legacy plaintext token fallback for backward compatibility
        return ciphertext
    
    try:
        parts = ciphertext.split(":")
        if len(parts) != 4:
            return ciphertext
        
        nonce = bytes.fromhex(parts[2])
        encrypted_data = bytes.fromhex(parts[3])
        decrypted_bytes = _aesgcm.decrypt(nonce, encrypted_data, None)
        return decrypted_bytes.decode("utf-8")
    except Exception as e:
        print(f"[Crypto Notice] Token decryption notice: {e}")
        return ""


def hash_token(raw_token: str) -> str:
    """
    Creates a SHA-256 hash of a session or refresh token for indexed database storage.
    """
    if not raw_token:
        return ""
    return hashlib.sha256(raw_token.encode("utf-8")).hexdigest()
