from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from kadinsky import create_image


router = Router()
# router.message.filter(F.chat.id == 1908725120)
router.message.filter(lambda message: message.message_thread_id == 204)

@router.message(F.text)
async def message_with_text(message: Message):
    await message.answer("Рисую...")
    path = await create_image(message.text, message.chat.id)
    photo = FSInputFile(f"{path}", "rb")
    await message.answer_photo(photo)
    await message.bot.delete_message(chat_id=message.chat.id, message_id=message.message_id+1)
