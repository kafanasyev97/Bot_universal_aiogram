from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp
from loguru import logger


@dp.message_handler(commands=['cancel'], state='*')
async def cancel(message: types.Message, state: FSMContext):
    """
    Прекращает состояния команд.

    :param message: Message
    :param state: FSMContext
    :return: None
    """
    current_state = await state.get_state()
    logger.info('Запрошена команда cancel.')
    if current_state is None:
        return
    await state.finish()
    await message.answer('Вы вышли из цикла команды.')
