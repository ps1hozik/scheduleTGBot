from aiogram import Router, types

router = Router(name=__name__)


@router.message()
async def delete_msg(message: types.Message):
    await message.delete()
