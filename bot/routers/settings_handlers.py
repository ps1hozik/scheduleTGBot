from aiogram import F, Router, types

from aiogram.filters import Command

import os
import sys
import logging
import asyncio


paths = ["../keyboards", "../schedule", "../database"]
for path in paths:
    sys.path.insert(1, os.path.join(sys.path[0], path))

from user import get_user


from keyboards.common_keyboards import (
    build_facultie_kb,
    main_kb,
)


router = Router(name=__name__)


@router.message(Command("keyboard"))
async def handle_keyboard(message: types.Message):
    await message.answer(text="Клавиатура отображена", reply_markup=main_kb())


@router.message(Command("current_group"))
async def handle_get_group(message: types.Message):
    user_id = message.from_user.id
    group = get_user(user_id)
    logging.info(user_id)
    await message.answer(
        text=f"Ваша группа:\n{group}",
        reply_markup=main_kb(),
    )


@router.message(Command("change_group"))
async def handle_course_number(message: types.Message):
    await message.answer(
        text="⚙️Настройка группы.\nВыберите факультет:",
        reply_markup=build_facultie_kb(),
    )
