import logging

from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

from filters.filters import MyTrueFilter, MyFalseFilter
from lexicon.lexicon_ru import LEXICON_RU

logger = logging.getLogger(__name__)

user_router = Router()

@user_router.message(CommandStart(), MyTrueFilter())
async def process_start_command(message: Message, i18n: dict[str, str]):
    logger.debug('Вошли в хэндлер, обрабатывающий команду /start')
    button = InlineKeyboardButton(text=i18n['button'], callback_data='button_pressed')
    markup = InlineKeyboardMarkup(inline_keyboard=[[button]])
    await message.answer(text=i18n['/start'], reply_markup=markup)
    logger.debug('Выходим из хэндлера, обрабатывающего команду /start')


@user_router.callback_query(F.data, MyTrueFilter())
async def process_button_click(callback: CallbackQuery):
    logger.debug('Вошли в хэндлер, обрабатывающий нажатие на инлайн-кнопку')
    await callback.answer(text=LEXICON_RU['button_pressed'])
    logger.debug('Выходим из хэндлера, обрабатывающего нажатие на инлайн-кнопку')


@user_router.message(F.text, MyFalseFilter())
async def process_text(message: Message):
    logger.debug('Вошли в хэндлер, обрабатывающий текст')
    logger.debug('Вышли из хэндлера, обрабатывающего текст')
