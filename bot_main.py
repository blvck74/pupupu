import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from aiogram.filters import Command
from aiogram import Router
from buttons import main_menu_keyboard
from config import TELEGRAM_TOKEN
from handlers import router as handlers_router

# Включаем логирование
logging.basicConfig(level=logging.INFO)

# Токен вашего бота
API_TOKEN = TELEGRAM_TOKEN

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
router = Router()

# Обработчик команды /start
@router.message(Command("start"))
async def send_welcome(message: Message):
    try:
        await message.delete()
    except Exception as e:
        logging.error(f"Ошибка при удалении сообщения: {e}")
    sent_message = await message.answer("Добро пожаловать! Выберите действие:", reply_markup=main_menu_keyboard)
    await asyncio.sleep(600)
    try:
        await bot.delete_message(chat_id=sent_message.chat.id, message_id=sent_message.message_id)
    except Exception as e:
        logging.error(f"Ошибка при удалении сообщения: {e}")

# Регистрация маршрутов
async def main():
    dp.include_router(router)
    dp.include_router(handlers_router)

    # Убедимся, что все обработчики зарегистрированы
    logging.info('Маршрутизатор успешно зарегистрирован')

    try:
        await dp.start_polling(bot, skip_updates=True)
    except Exception as e:
        logging.error(f"Ошибка при запуске бота: {e}")

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception as e:
        logging.error(f"Ошибка при запуске основного цикла: {e}")
