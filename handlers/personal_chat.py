import asyncio
from aiogram.filters import Command
from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from kadinsky import create_image




router = Router()
router.message.filter(F.chat.type == "private")
queue = asyncio.Queue()


@router.message(Command("start")) 
async def cmd_start(message: Message):
    await message.answer("Привет, я Кандинский и могу нарисовать, то что ты захочешь 🎨")


@router.message(F.text)
async def message_with_text(message: Message):
    await message.answer(f"Рисую...")
    path = await create_image(message.text, message.chat.id)
    photo = FSInputFile(f"{path}", "rb")
    print(f"Done {message.text}")
    await message.reply_photo(photo)

        

