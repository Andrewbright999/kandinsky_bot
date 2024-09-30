import logging
import asyncio

from aiogram import Bot, Dispatcher
from handlers.personal_chat import router as personal_router
from handlers.xyapi_chat import router as xyapi_router

from config import TG_TOKEN


logging.basicConfig(level=logging.INFO)

bot = Bot(token=TG_TOKEN)
dp = Dispatcher()

# Запуск бота
async def main():
    dp.include_routers(xyapi_router, personal_router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
