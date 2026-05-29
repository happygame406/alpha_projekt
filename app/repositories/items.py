from sqlmodel import select, func
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.items import Item, ItemCreate, ItemUpdate
from app.models.users import User


async def create_item_repository(session, user: User, item_data: ItemCreate):
    """Создание нового объявления"""
    item = Item(
        title=item_data.title,
        description=item_data.description,
        price=item_data.price,
        user_id=user.id
    )
    
    session.add(item)
    session.commit()        # без await
    session.refresh(item)   # без await
    return item


def list_items_with_count(session, q: str = None, user_id: int = None, limit: int = 20, offset: int = 0):
    """Получение списка товаров с подсчётом количества"""
    statement = select(Item)
    
    if user_id is not None:
        statement = statement.where(Item.user_id == user_id)
    if q:
        statement = statement.where(Item.title.ilike(f"%{q}%"))
    
    # Получаем товары
    items = session.exec(statement.limit(limit).offset(offset)).all()
    
    # Получаем количество
    count_statement = select(func.count()).select_from(
        select(Item.id)
        .where(statement.whereclause if hasattr(statement, 'whereclause') and statement.whereclause is not None else True)
        .subquery()
    )
    
    count_result = session.exec(count_statement).first()
    count = count_result[0] if isinstance(count_result, (list, tuple)) else (count_result or 0)
    
    return items, count


async def get_item(session, item_id: int):
    return await session.get(Item, item_id)


async def patch_item(session, item_db: Item, item_data: ItemUpdate):
    data = item_data.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(item_db, key, value)
    
    session.add(item_db)
    session.commit()      # без await
    session.refresh(item_db)
    return item_db


async def delete_item(session, item: Item):
    session.delete(item)
    session.commit()      # без await
    return item