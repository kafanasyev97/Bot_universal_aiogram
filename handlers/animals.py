from aiogram import types
from loader import dp, bot
import random
from loguru import logger


@dp.message_handler(commands=['animals'])
async def start(message: types.Message):
    """
    Команда отправки ботом случайного фото милых животных.

    :param message: Message
    :return: None
    """
    with open(f'media/photo{random.randint(1, 5)}.jpeg', 'rb') as photo:
        await bot.send_photo(chat_id=message.from_user.id, photo=photo)
    logger.info('Запрошена команда animals.')
