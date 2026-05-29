from sqlmodel import select, func
from app.models.users import User, UserCreate, UserUpdate
from app.database import SessionDep
from app.utils.password import get_password_hash

# ====================== ПОЛЬЗОВАТЕЛИ ======================

def list_users_with_count(
    session: SessionDep, 
    q: str | None = None, 
    is_active: bool | None = None, 
    limit: int = 20, 
    offset: int = 0
):
    """Простая версия без сложного подсчёта"""
    statement = select(User)
    
    if q:
        statement = statement.where(User.username.ilike(f"%{q}%"))
    
    if is_active is not None:
        statement = statement.where(User.is_active == is_active)
    
    statement = statement.offset(offset).limit(limit)
    
    result = session.exec(statement)
    users = result.all()
    
    # Простой подсчёт (чтобы не падало)
    count = len(users)
    
    return users, count


def get_user(session: SessionDep, user_id: int):
    """Получение пользователя по ID"""
    result = session.exec(
        select(User).where(User.id == user_id)
    )
    return result.first()


def get_user_by_username(session: SessionDep, username: str):
    """Получение пользователя по username"""
    result = session.exec(
        select(User).where(User.username == username)
    )
    return result.first()


def update_user(session: SessionDep, db_user: User, user_in: UserUpdate) -> User:
    data = user_in.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(db_user, key, value)
    
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def delete_user(session: SessionDep, user: User):
    session.delete(user)
    session.commit()


def create_user_repository(session: SessionDep, user_data: UserCreate):
    """Создание пользователя"""
    hashed_password = get_password_hash(user_data.password)
    
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password,
        is_active=True
    )
    
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user