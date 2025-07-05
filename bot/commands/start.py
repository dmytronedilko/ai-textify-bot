from aiogram import Router, types
from aiogram.filters import Command

router = Router()


@router.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer("Hi! Send me a voice message to get started.")
