import bcrypt

from app.application.interfaces.password_hasher import IPasswordHasher


class PasswordHasherImp(IPasswordHasher):
    @staticmethod
    def hash_password(password: str) -> str:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        result = bcrypt.checkpw(password.encode(), hashed_password.encode())
        return result
