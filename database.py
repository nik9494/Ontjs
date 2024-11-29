from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
import os
from dotenv import load_dotenv
import asyncpg
from urllib.parse import urlparse

# Загрузка переменных окружения
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Инициализация асинхронного движка
engine = create_async_engine(DATABASE_URL, echo=True)  # Используем create_async_engine для создания асинхронного движка

# Создание асинхронной сессии через async_sessionmaker
async_session = async_sessionmaker(
    engine,  # Указываем асинхронный движок
    class_=AsyncSession,  # Используем AsyncSession для асинхронных сессий
    expire_on_commit=False  # Отключаем автоматическое обновление объектов после commit
)

# Базовая модель
Base = declarative_base()

# Зависимость для получения сессии
async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session

async def create_database_if_not_exists():
    """Проверка существования базы данных и создание её при необходимости."""
    parsed_url = urlparse(DATABASE_URL)
    user = parsed_url.username
    password = parsed_url.password
    host = parsed_url.hostname
    port = parsed_url.port
    database = parsed_url.path.lstrip('/')

    # Создание подключения к базе данных PostgreSQL для проверки существования базы
    conn = await asyncpg.connect(user=user, password=password, database="postgres", host=host, port=port)
    try:
        result = await conn.fetch(f"SELECT 1 FROM pg_database WHERE datname='{database}'")
        if not result:
            await conn.execute(f"CREATE DATABASE {database}")
            print(f"Database {database} created.")
    finally:
        await conn.close()

async def init_db():
    """Инициализация базы данных."""
    await create_database_if_not_exists()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)  # Создаем все таблицы
    print("Database initialized and schema created.")
