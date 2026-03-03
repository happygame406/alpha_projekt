import asyncio
from app.database import engine
from app.models.users import User
from app.models.items import Item
from sqlmodel import SQLModel

async def init_database():
    print("=" * 50)
    print("СОЗДАНИЕ БАЗЫ ДАННЫХ")
    print("=" * 50)
    
    try:
        # Создаем все таблицы
        async with engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
        print("✅ Таблицы успешно созданы!")
        
        # Проверяем, какие таблицы создались
        async with engine.connect() as conn:
            from sqlalchemy import inspect
            inspector = await conn.run_sync(inspect)
            tables = await conn.run_sync(inspector.get_table_names)
            print(f"📊 Таблицы в базе: {', '.join(tables)}")
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    
    print("=" * 50)

if __name__ == "__main__":
    asyncio.run(init_database())