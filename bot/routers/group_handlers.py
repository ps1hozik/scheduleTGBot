from aiogram import F, Router, types
from aiogram.types import CallbackQuery
from aiogram.filters import CommandStart

import os
import sys
import logging


paths = ["../keyboards", "../schedule", "../database"]
for path in paths:
    sys.path.insert(1, os.path.join(sys.path[0], path))

from scripts import get_groups, get_subgroups
from user import insert
from config import get_database

from keyboards.common_keyboards import (
    build_facultie_kb,
    build_course_kb,
    build_group_kb,
    main_kb,
    ButtonText,
)


router = Router(name=__name__)


@router.message(CommandStart())
async def handle_start(message: types.Message):
    dbname = get_database()
    collection_user = dbname["users"]
    user = collection_user.find_one({"user_id": message.from_user.id})
    if not user:
        await message.answer(
            text="⚙️Настройка группы.\nВыберите факультет:",
            reply_markup=build_facultie_kb(),
        )
    else:
        await message.answer(
            text=f"С возвращением <i><b>{message.from_user.full_name}</b></i> 👋",
            reply_markup=main_kb(),
        )


class Group:
    facultie = ""
    groups = []
    subgroups = []


@router.callback_query(F.data.in_(ButtonText.FACULTIES.keys()))
async def handle_course_number(callback_query: CallbackQuery):
    await callback_query.answer()

    Group.facultie = ButtonText.FACULTIES.get(callback_query.data)
    await callback_query.message.edit_text(
        text=f"Выберите курс:",
        reply_markup=build_course_kb(),
    )


@router.callback_query(F.data.in_(ButtonText.COURSES))
async def handle_group(callback_query: CallbackQuery):
    await callback_query.answer()
    data = callback_query.data.strip()
    number = int(data[0])
    facultie = Group.facultie
    groups = get_groups(facultie, number)
    Group.groups = groups
    await callback_query.message.edit_text(
        text=f"Выберите группу:",
        reply_markup=build_group_kb(groups),
    )


@router.message(F.text == ButtonText.CHANGE_FACULTIE)
async def handle_change_facultie(message: types.Message):
    settings_text = "⚙️ Выберите факультет:"
    await message.answer(
        text=settings_text,
        reply_markup=build_facultie_kb(),
    )


@router.callback_query()
async def handle_group_number(callback_query: CallbackQuery):
    if callback_query.data in Group.groups:
        await callback_query.answer()
        subgroups = get_subgroups(Group.facultie, callback_query.data)
        Group.subgroups = subgroups
        await callback_query.message.edit_text(
            text=f"Выберите подгруппу:",
            reply_markup=build_group_kb(subgroups),
        )
    if callback_query.data in Group.subgroups:
        user_id = callback_query.from_user.id
        group = callback_query.data
        insert(user_id, group, Group.facultie)
        await callback_query.message.answer(
            text="Теперь вам доступно расписание",
            reply_markup=main_kb(),
        )
        await callback_query.message.edit_text(
            text=f"Вы выбрали группу: <i><b>{group}</b></i>",
        )
    if "count" in callback_query.data:
        user_id = callback_query.from_user.id
        lesson_count = int(callback_query.data.split()[1])
        insert(user_id=user_id, lesson_count=lesson_count)
        await callback_query.message.edit_text(
            text=f"Теперь в расписании будет отображено <i><b>{lesson_count}</b></i> пар",
        )
