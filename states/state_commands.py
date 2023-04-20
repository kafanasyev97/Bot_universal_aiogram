from aiogram.dispatcher.filters.state import StatesGroup, State


class WeatherState(StatesGroup):
    """
    Машина состояний для команды weather.
    """
    city = State()


class ConvertState(StatesGroup):
    """
    Машина состояний для команды convert.
    """
    first_value = State()
    second_value = State()
    amount = State()


class PollState(StatesGroup):
    """
    Машина состояний для команды poll.
    """
    question = State()
    answers = State()
