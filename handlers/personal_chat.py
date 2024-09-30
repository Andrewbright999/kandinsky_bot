from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from queue_module import handle_prompt


router = Router()
router.message.filter(F.chat.type == "private")


@router.message(Command("start"))
async def send_welcome(message: Message):
    await message.answer("Привет! Отправь мне промт, и я сгенерирую изображение на его основе!")

# Обработчик сообщений с промтами
@router.message()
async def handle_message(message: Message):

    await handle_prompt(message)
