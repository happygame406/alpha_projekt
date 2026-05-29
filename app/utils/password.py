import hashlib

def get_password_hash(password: str) -> str:
    """Простое, но надёжное хэширование (для учебного проекта)"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверка пароля"""
    return get_password_hash(plain_password) == hashed_password