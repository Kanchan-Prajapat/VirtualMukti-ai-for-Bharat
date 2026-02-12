"""Authentication service with JWT and bcrypt"""

from datetime import datetime, timedelta
from typing import Optional
import bcrypt
from jose import JWTError, jwt

from ..config import settings
from ..models.user import UserCreate
from ..repositories.user_repository import UserRepository


class AuthService:
    """Authentication service for user registration and login"""

    # -----------------------
    # Password helpers
    # -----------------------
    @staticmethod
    def hash_password(password: str) -> str:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
        return hashed.decode("utf-8")

    @staticmethod
    def verify_password(password: str, password_hash: str) -> bool:
        return bcrypt.checkpw(
            password.encode("utf-8"),
            password_hash.encode("utf-8"),
        )

    # -----------------------
    # JWT helpers
    # -----------------------
    @staticmethod
    def create_jwt_token(user_id: str, username: str) -> str:
        expiration = datetime.utcnow() + timedelta(
            hours=settings.jwt_expiration_hours
        )

        payload = {
            "sub": user_id,
            "username": username,
            "exp": expiration,
            "iat": datetime.utcnow(),
        }

        return jwt.encode(
            payload,
            settings.jwt_secret_key,
            algorithm=settings.jwt_algorithm,
        )

    @staticmethod
    def validate_token(token: str) -> Optional[dict]:
        try:
            payload = jwt.decode(
                token,
                settings.jwt_secret_key,
                algorithms=[settings.jwt_algorithm],
            )
            return {
                "user_id": payload.get("sub"),
                "username": payload.get("username"),
            }
        except JWTError:
            return None

    # -----------------------
    # Register
    # -----------------------
    @staticmethod
    async def register(user_data: UserCreate) -> dict:
        username = user_data.username.lower()

        if await UserRepository.username_exists(username):
            raise ValueError("Username already exists")

        password_hash = AuthService.hash_password(user_data.password)

        user = await UserRepository.create(
            user=user_data,
            password_hash=password_hash,
        )

        token = AuthService.create_jwt_token(
            user["id"],
            user["username"],
        )

        return {
            "success": True,
            "user_id": user["id"],
            "username": user["username"],
            "token": token,
        }

# -----------------------
# Login
# -----------------------
    @staticmethod
    async def login(username: str, password: str) -> dict:
        username = username.lower()
        print("🔐 LOGIN ATTEMPT:", username)

        user = await UserRepository.get_by_username(username)
        print("👤 USER FROM DB:", user)

        if user is None:
            print("❌ USER NOT FOUND")
            raise ValueError("Invalid credentials")

        print("🔑 INPUT PASSWORD:", password)
        print("🔑 STORED HASH:", user.password_hash)
        if not AuthService.verify_password(password, user.password_hash):
            print("❌ PASSWORD MISMATCH")
            raise ValueError("Invalid credentials")

        await UserRepository.update_last_login(user.id)

        token = AuthService.create_jwt_token(user.id, user.username)

        print("✅ LOGIN SUCCESS")

        return {
        "success": True,
        "user_id": user.id,
        "username": user.username,
        "token": token,
    }
