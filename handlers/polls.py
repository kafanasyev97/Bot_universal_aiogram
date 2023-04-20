from aiogram.dispatcher import FSMContext
from loader import dp, bot
from aiogram import types
from states.state_commands import PollState
from loguru import logger


@dp.message_handler(commands=['poll'], state=None)
async def poll_command(message: types.Message):
    """
    Принимает команду для создания опроса и переходит в состояние.

    :param message: Message
    :return: None
    """
    await PollState.question.set()
    await message.answer(text='Введите вопрос для опроса:')
    logger.info('Введена команда poll. Начинаем состояние.')


@dp.message_handler(state=PollState.question)
async def poll_start(message: types.Message, state: FSMContext):
    """
    Записывает вопрос для опроса в словарь.

    :param message: Message
    :param state: FSMContext
    :return: None
    """
    async with state.proxy() as data:
        data['question'] = message.text
    await message.answer(text='Введите варианты ответа через точку с запятой:')
    await PollState.next()
    logger.info('Записали вопрос в словарь.')


@dp.message_handler(state=PollState.answers)
async def poll_finish(message: types.Message, state: FSMContext):
    """
    Выводит опрос, заданный пользователем, в чат, в котором были заданы параметры для опроса.

    :param message: Message
    :param state: FSMContext
    :return: None
    """
    try:
        answers = message.text.split(';')
        options = []
        index = 1
        for elem in answers:
            options.append(f'{index}) {elem}')
            index += 1
        async with state.proxy() as data:
            question = data['question']
        await bot.send_poll(
            chat_id=message.chat.id,
            question=question,
            options=options,
            type='regular',
            is_anonymous=False
        )
        logger.info('Вывели опрос в чат.')
        await state.finish()
    except Exception:
        await message.answer(text='Введите ответы через точку с запятой!')
        logger.error('Неправильный ввод ответов.')
