import os
import logging
from fastapi import FastAPI, Request, APIRouter, Depends
from contextlib import asynccontextmanager
from dotenv import load_dotenv

# Telegram и Aiogram
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Update
from sqlalchemy.ext.asyncio import AsyncSession

# Импорт моделей и движка из database.py
from database import engine, get_session, Base  # Исправлено: импорт get_session и Base
from models import User  # Импорт модели User

# Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Загрузка переменных окружения
load_dotenv()

# Конфигурация
BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "https://your-server.com/webhook/")

if not all([BOT_TOKEN, DATABASE_URL]):
    raise ValueError("Необходимо указать BOT_TOKEN и DATABASE_URL в .env")

# Инициализация
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
api_router = APIRouter()

# Зависимость для получения сессии
# Используем get_session из database.py
# async def get_session() -> AsyncSession:  # Удалено, так как уже импортировано
#     async with async_session() as session:
#         yield session

# Базовые маршруты Telegram
@dp.message(Command("start"))
async def send_welcome(message: types.Message, session: AsyncSession = Depends(get_session)):
    try:
        # Сохраняем пользователя в базу данных (модель User уже определена)
        user = User(
            telegram_id=message.from_user.id,
            name=message.from_user.first_name,  # Пример поля, которое можно добавить
            role="user"  # Пример значения для поля роли
        )
        session.add(user)
        await session.commit()

        await message.answer("Привет! Бот успешно запущен и сохранил вашу информацию.")
    except Exception as e:
        logger.error(f"Ошибка при сохранении пользователя: {e}")
        await message.answer("Произошла ошибка при регистрации.")

# Webhook обработчик
@api_router.post("/webhook/")
async def handle_webhook(request: Request):
    try:
        data = await request.json()
        update = Update(**data)
        await dp.feed_update(bot=bot, update=update)
        return {"status": "ok"}
    except Exception as e:
        logger.error(f"Ошибка webhook: {e}")
        return {"status": "error"}

# Жизненный цикл приложения
@asynccontextmanager
async def lifespan(application: FastAPI):
    global app
    app = application

    # Создание таблиц при старте
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Установка webhook
    await bot.set_webhook(WEBHOOK_URL)

    yield

    # Закрытие webhook при остановке
    await bot.delete_webhook()

# Основное FastAPI приложение
app = FastAPI(lifespan=lifespan)

# Подключение роутеров
app.include_router(api_router)

# Корневой маршрут
@app.get("/")
async def root():
    return {"message": "Telegram Bot API готов к работе"}

# Запуск приложения
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
