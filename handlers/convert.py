from aiogram.dispatcher import FSMContext
from loader import dp, API_KEY_CONVERT
from aiogram import types
import requests
from states.state_commands import ConvertState
from loguru import logger


@dp.message_handler(commands=['convert'], state=None)
async def convert_command(message: types.Message):
    """
    Принимает команду для конвертации валют и переходит в состояние.

    :param message: Message
    :return: None
    """
    await ConvertState.first_value.set()
    await message.answer(text='Введите код валюты, из которой будем конвертировать:')
    logger.info('Запрошена команда convert. Начинаем состояние.')


@dp.message_handler(state=ConvertState.first_value)
async def convert_first(message: types.Message, state: FSMContext):
    """
    Проверяет введенный код валюты на корректность и записывает его в словарь.

    :param message: Message
    :param state: FSMContext
    :return: None
    """
    if len(message.text) == 3 and message.text.isalpha():
        async with state.proxy() as data:
            data['from'] = message.text.upper()
        await message.answer(text='Теперь код валюты, в которую будем конвертировать:')
        await ConvertState.next()
        logger.info('Узнаем начальную валюту.')
    else:
        await message.answer(text='Код должен состоять из 3 букв!')
        logger.error('Введены некорректные данные валюты!')


@dp.message_handler(state=ConvertState.second_value)
async def convert_second(message: types.Message, state: FSMContext):
    """
    Проверяет введенный код валюты на корректность и записывает его в словарь.

    :param message: Message
    :param state: FSMContext
    :return: None
    """
    if len(message.text) == 3 and message.text.isalpha():
        async with state.proxy() as data:
            data['to'] = message.text.upper()
        await message.answer(text='Введите сумму:')
        await ConvertState.next()
        logger.info('Узнаем конечную валюту.')
    else:
        await message.answer(text='Код должен состоять из 3 цифр!')
        logger.error('Введены некорректные данные валюты!')


@dp.message_handler(state=ConvertState.amount)
async def weather_finish(message: types.Message, state: FSMContext):
    """
    Выводит результат конвертации, делая запрос к API сайта.

    :param message: Message
    :param state: FSMContext
    :return: None
    """
    if message.text.isdigit():
        try:
            amount = message.text
            async with state.proxy() as data:
                from_value = data['from']
                to_value = data['to']
            url = f'https://api.apilayer.com/exchangerates_data/convert?to={to_value}&from={from_value}&amount={amount}'
            headers = {
                "apikey": API_KEY_CONVERT
            }
            response = requests.request("GET", url, headers=headers)
            result = response.json()['result']
            await message.answer(text=f"Результат: {round(result, 2)} {to_value}")
            logger.info('Выводим пользователю результат конвертации.')
            await state.finish()
        except KeyError:
            await message.answer(text='Вы ошиблись в написании валюты. '
                                      'Введите еще раз код валюты, из которой будем конвертировать:')
            logger.error('Ошибка в правильности написании валюты. Начинаем заново.')
            await ConvertState.first_value.set()

    else:
        await message.answer(text='Укажите число!')
        logger.error('Введены некорректные данные суммы!')
