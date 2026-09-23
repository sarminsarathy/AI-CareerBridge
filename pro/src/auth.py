import hashlib
import secrets
import hmac
import json
import base64
import time

SECRET_KEY = "careerbridge_secure_jwt_secret_key_2026_antigravity"

def hash_password(password: str) -> str:
    """Hashes a password using PBKDF2 with SHA256 and a secure salt."""
    salt = secrets.token_hex(16)
    key = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        100000
    )
    return f"{salt}${key.hex()}"

def verify_password(password: str, stored_password_hash: str) -> bool:
    """Verifies a password against the stored salt$hash string."""
    try:
        salt, stored_hash = stored_password_hash.split('$')
        key = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000
        )
        return secrets.compare_digest(key.hex(), stored_hash)
    except Exception:
        return False

def _b64_encode(data_bytes: bytes) -> str:
    return base64.urlsafe_b64encode(data_bytes).decode('utf-8').rstrip('=')

def _b64_decode(data_str: str) -> bytes:
    padding = '=' * (4 - (len(data_str) % 4))
    return base64.urlsafe_b64decode(data_str + padding)

def generate_token(user_id: int, email: str, expires_in_seconds: int = 86400 * 7) -> str:
    """Generates an HMAC-signed JWT token."""
    header = {"alg": "HS256", "typ": "JWT"}
    payload = {
        "sub": user_id,
        "email": email,
        "exp": int(time.time()) + expires_in_seconds
    }
    
    header_b64 = _b64_encode(json.dumps(header).encode('utf-8'))
    payload_b64 = _b64_encode(json.dumps(payload).encode('utf-8'))
    
    signature_input = f"{header_b64}.{payload_b64}".encode('utf-8')
    signature = hmac.new(SECRET_KEY.encode('utf-8'), signature_input, hashlib.sha256).digest()
    sig_b64 = _b64_encode(signature)
    
    return f"{header_b64}.{payload_b64}.{sig_b64}"

def verify_token(token: str):
    """Verifies HMAC signature and expiration, returns payload dict or None."""
    try:
        parts = token.split('.')
        if len(parts) != 3:
            return None
        
        header_b64, payload_b64, sig_b64 = parts
        signature_input = f"{header_b64}.{payload_b64}".encode('utf-8')
        expected_sig = hmac.new(SECRET_KEY.encode('utf-8'), signature_input, hashlib.sha256).digest()
        
        if not secrets.compare_digest(_b64_encode(expected_sig), sig_b64):
            return None
        
        payload_json = _b64_decode(payload_b64).decode('utf-8')
        payload = json.loads(payload_json)
        
        if payload.get("exp", 0) < time.time():
            return None
        
        return payload
    except Exception:
        return None
