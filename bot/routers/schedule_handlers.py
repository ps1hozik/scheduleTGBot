from aiogram import F, Router, types
from aiogram.filters import Command
import os
import sys
from datetime import timedelta, datetime
import pytz


paths = ["../keyboards", "../schedule", "../database"]
for path in paths:
    sys.path.insert(1, os.path.join(sys.path[0], path))

from scripts import get_all, get_one_day, find_teacher


from keyboards.common_keyboards import (
    main_kb,
    ButtonText,
)


router = Router(name=__name__)


@router.message(F.text == ButtonText.TODAY)
async def handle_today(message: types.Message):
    current_utc_time = datetime.now(pytz.timezone("UTC"))
    moscow_timezone = pytz.timezone("Europe/Moscow")
    moscow_time = current_utc_time.astimezone(moscow_timezone)

    moscow_date = str(moscow_time.date())
    schedule = get_one_day(message.from_user.id, moscow_date)
    await message.answer(
        text=schedule or "На сегодня расписания нет 😽",
        reply_markup=main_kb(),
    )


async def get_tommorow_schedule(user_id):
    current_utc_time = datetime.now(pytz.timezone("UTC")) + timedelta(days=1)
    moscow_timezone = pytz.timezone("Europe/Moscow")
    moscow_time = current_utc_time.astimezone(moscow_timezone)

    moscow_date = str(moscow_time.date())
    schedule = get_one_day(user_id, moscow_date)
    return schedule or "На завтра расписания нет 😽"


@router.message(F.text == ButtonText.TOMMOROW)
async def handle_tommorow(message: types.Message):
    schedule = await get_tommorow_schedule(message.from_user.id)
    await message.answer(
        text=schedule,
        reply_markup=main_kb(),
    )


@router.message(F.text == ButtonText.ALL_WEEK)
async def handle_all_week(message: types.Message):
    schedule = get_all(message.from_user.id)
    if not schedule:
        await message.answer(
            text="На этой недели расписания нет 😽",
            reply_markup=main_kb(),
        )
    else:
        for item in schedule:
            await message.answer(
                text=item,
                reply_markup=main_kb(),
            )


@router.message(Command("find"))
async def handle_find_teacher(message: types.Message):

    parts = message.text.split(maxsplit=1)[1]
    if len(parts) > 1:
        teacher_name = parts[1]
        schedule = find_teacher(teacher_name)
        if not schedule:
            await message.answer(
                text=f"Не нашли расписание для <i><u>{teacher_name}</u></i>",
                reply_markup=main_kb(),
            )
        else:
            for item in schedule:
                await message.answer(
                    text=item,
                    reply_markup=main_kb(),
                )
    else:
        await message.reply(
            "Пожалуйста, укажите ФИО. Например: /find_teacher Иванов И И"
        )
