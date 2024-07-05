import asyncio, logging, sys
from aiogram import Bot, Dispatcher
# from aiogram.client.session.aiohttp import AiohttpSession
from handlers import personal_chat, xyapi_chat
from config import TG_TOKEN

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TG_TOKEN)
dp = Dispatcher()
# dp.message.filter(lambda message: message.from_user.is_bot == True)

async def main() -> None:
    dp.include_routers(personal_chat.router, xyapi_chat.router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

# try:
#     session = AiohttpSession(proxy='http://proxy.server:3128')
#     bot = Bot(token=TG_TOKEN, session=session)
# except:
#     bot = Bot(token=TG_TOKEN)
