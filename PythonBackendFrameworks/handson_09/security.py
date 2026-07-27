"""
security.py - Handles password hashing and JWT token operations.

Why bcrypt?
  - bcrypt is a slow hashing algorithm designed specifically for passwords.
  - Its work factor (salt rounds) can be increased as hardware gets faster,
    keeping brute-force attacks expensive.
  - Unlike SHA-256/MD5, bcrypt automatically includes a random salt,
    preventing rainbow table attacks.

JWT Authentication Flow:
  1. User registers with email + password (password is hashed and stored).
  2. User logs in: server verifies password hash, then issues a signed JWT access token.
  3. Client sends JWT in Authorization header: "Bearer <token>"
  4. Server decodes and validates the token on every protected request.
  5. No session is stored server-side - JWT is stateless.

OAuth2 Authorization Code Flow (for reference):
  - Used when a 3rd-party app needs access on behalf of a user.
  - Step 1: Redirect user to Authorization Server (e.g., Google).
  - Step 2: User logs in and grants permission.
  - Step 3: Authorization server redirects back with a short-lived "code".
  - Step 4: App exchanges code for access_token + refresh_token.
  - Step 5: Access token used to call protected APIs.
  - Difference from JWT login: OAuth2 involves a 3rd party auth server; JWT login is self-contained.
"""

from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
import bcrypt

SECRET_KEY = "your-super-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def hash_password(plain_password: str) -> str:
    """Returns the bcrypt hash of a plain text password.
    Using the bcrypt library directly for Python 3.14 compatibility.
    """
    password_bytes = plain_password.encode('utf-8')
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain password against a stored bcrypt hash."""
    password_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """Creates a signed JWT access token with an expiry time."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict:
    """Decodes and validates a JWT token. Raises JWTError if invalid or expired."""
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
