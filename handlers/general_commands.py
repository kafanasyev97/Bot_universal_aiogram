from aiogram import types
from loader import dp
from loguru import logger


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    """
    Команда приветствия пользователя.

    :param message: Message
    :return: None
    """
    await message.answer(f'Привет {message.from_user.first_name}! Для просмотра команд бота введи /help')


@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    """
    Выводит список команд бота.

    :param message: Message
    :return: None
    """
    text = """
        Команды бота:
        /weather - узнать погоду в выбранном городе
        /convert - произвести конвертацию валюты
        /cancel - завершает работу команд
        /animals - отправляет случайную картинку с милыми животными
        /poll - создает опрос
        """
    await message.answer(text=text)
    logger.info('Запрошена команда help.')


@dp.message_handler(content_types=['photo'], state='*')
async def photo_weather(message: types.Message):
    """
    Выводит сообщение, если пользователь отправляет боту фотографию.

    :param message: Message
    :return: None
    """
    await message.reply(text='Фото не подходит!')
    logger.info('Пользователь отправил фото.')


@dp.message_handler()
async def unknown(message: types.Message):
    """
    Реагирует на любое неизвестное сообщение.

    :param message: Message
    :return: None
    """
    await message.answer('Такого сообщения я не знаю.')
    logger.info('Неизвестное сообщение.')
