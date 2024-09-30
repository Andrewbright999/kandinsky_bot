from aiogram import Router
from aiogram.types import Message
from queue_module import handle_prompt


router = Router()
# router.message.filter(F.chat.id == 1908725120)
router.message.filter(lambda message: message.message_thread_id == 204)

@router.message()
async def handle_message(message: Message):
    
    await handle_prompt(message)
