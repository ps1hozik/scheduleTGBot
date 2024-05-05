from aiogram.types import (
    KeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder


class ButtonText:
    TODAY = "Сегодня"
    TOMMOROW = "Завтра"
    ALL_WEEK = "Вся неделя"
    GET_GROUP = "Текущаяя группа"
    COURSES = [
        "1️⃣",
        "2️⃣",
        "3️⃣",
        "4️⃣",
    ]
    FACULTIES = {
        "ped": "Педагогический факультет",
        "gum": "Факультет гуманитаристики и языковых коммуникаций",
        "fmiit": "Факультет математики и информационных технологий",
        "soc": "Факультет социальной педагогики и психологии",
        "fiz": "Факультет физической культуры и спорта",
        "him": "Факультет химико-биологических и географических наук",
        "hud": "Художественно-графический факультет",
        "ur": "Юридический факультет",
    }
    CHANGE_FACULTIE = "⚙️ Изменить факультет"


def build_facultie_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for (data, facultie) in ButtonText.FACULTIES.items():
        builder.button(text=facultie, callback_data=data)
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True, input_field_placeholder=" ")


def build_course_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for course in ButtonText.COURSES:
        builder.button(text=course, callback_data=course)
    return builder.as_markup(resize_keyboard=True, input_field_placeholder=" ")


def build_group_kb(groups: list) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for group in groups:
        builder.button(text=group, callback_data=group)
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True, input_field_placeholder=" ")


def main_kb() -> ReplyKeyboardMarkup:
    button_today = KeyboardButton(text=ButtonText.TODAY)
    button_tommorow = KeyboardButton(text=ButtonText.TOMMOROW)
    button_week = KeyboardButton(text=ButtonText.ALL_WEEK)
    buttons_first_row = [button_today, button_tommorow]
    buttons_second_row = [button_week]
    markup = ReplyKeyboardMarkup(
        keyboard=[buttons_first_row, buttons_second_row],
        resize_keyboard=True,
        input_field_placeholder=" ",
    )
    return markup
