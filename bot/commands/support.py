from aiogram import Router, types
from aiogram.filters import Command

from services.get_user_locale import get_user_locale

router = Router()


@router.message(Command("support"))
async def support_command(message: types.Message):
    locale = await get_user_locale(message.from_user.id)
    await message.answer(locale["support_message"], parse_mode="HTML")
