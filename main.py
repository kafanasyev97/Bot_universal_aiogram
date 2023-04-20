import atexit
from aiogram import executor
from loader import dp
import handlers
from loguru import logger


@atexit.register
def goodbye() -> None:
    """
    Выводит сообщение при выходе
    """
    logger.info('Завершение работы бота.')


if __name__ == '__main__':
    logger.add('loguru_bot.log', rotation="100 MB", encoding='utf-8')
    logger.info('Запуск бота.')
    executor.start_polling(dp, skip_updates=True)
