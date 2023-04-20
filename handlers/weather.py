from aiogram.dispatcher import FSMContext
from loader import dp, API_KEY_WEATHER
from aiogram import types
import requests
from states.state_commands import WeatherState
from loguru import logger


@dp.message_handler(commands=['weather'], state=None)
async def weather_command(message: types.Message):
    """
    Принимает команду для вывода погоды и переходит в состояние.

    :param message: Message
    :return: None
    """
    await WeatherState.city.set()
    await message.answer(text='Введите город:')
    logger.info('Введена команда weather. Начинаем состояние.')


@dp.message_handler(state=WeatherState.city)
async def weather_finish(message: types.Message, state: FSMContext):
    """
    Делает запрос к API сайта с погодой и выводит пользователю температуру в указанном городе.

    :param message: Message
    :param state: FSMContext
    :return: None
    """
    try:
        city = message.text
        response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY_WEATHER}'
                                f'&units=metric')
        result = response.json()['main']['temp']
        async with state.proxy() as data:
            data['city'] = message.text
        await message.answer(text=f'Температура в городе {city.capitalize()}: {result} градусов.')
        logger.info('Выводим температуру пользователю.')
        await state.finish()
    except KeyError:
        await message.answer(text='Такого города нет! Введите другой город:')
        logger.error('Введен неизвестный город.')
