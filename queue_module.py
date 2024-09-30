import asyncio
from kadinsky import generate_image
from aiogram.types import BufferedInputFile, Message



async def handle_prompt(message: Message, prompt=None, queue_message=None):
    prompt = prompt or message.text
    account_index = None

    # Проверяем, есть ли свободный аккаунт
    for i in range(len(account_busy)):
        if not account_busy[i]:
            account_index = i
            account_busy[i] = True
            break

    if account_index is None:
        # Отправляем сообщение о том, что оба аккаунта заняты
        queue_message = await message.answer("Сейчас дорисую всё из очереди, и примусь за ваш запрос")
        waiting_queue.append((message, prompt, queue_message))
    else:
        # Отправляем сообщение о начале генерации и сохраняем его для последующего удаления
        status_message = await message.answer(f"Рисую...")

        # Запускаем генерацию
        asyncio.create_task(handle_generation(prompt, message, account_index, status_message, queue_message))


async def handle_generation(prompt, message: Message, account_index, status_message, queue_message=None):
    try:
        # Генерация изображения
        image_data = await generate_image(prompt, account_index)

        # Удаляем сообщение о начале генерации
        await status_message.delete()

        # Если было сообщение о занятости всех аккаунтов, удаляем его
        if queue_message:
            await queue_message.delete()

        # Отправка изображения пользователю в ответ на промт
        await message.bot.send_photo(
            message.chat.id,
            BufferedInputFile(image_data, filename="generated_image.jpg"),
            caption="Вот ваше произведение!",
            reply_to_message_id=message.message_id
        )
    finally:
        # Освобождаем аккаунт
        account_busy[account_index] = False

        # Проверяем, есть ли кто-то в очереди ожидания
        if waiting_queue:
            next_message, next_prompt, next_queue_message = waiting_queue.pop(0)

            asyncio.create_task(handle_prompt(next_message, next_prompt, next_queue_message))



account_busy = [False, False]
waiting_queue = []
