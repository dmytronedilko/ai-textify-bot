from aiogram import Router, types
from aiogram.filters import Command

router = Router()


@router.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer(
        "👋 Welcome to Textify!\n\n"
        "🎤 Just send a voice message — I’ll transcribe it for you.\n"
        "📌 In groups, use the /textify command to transcribe replies.\n\n"
        "❓ Need assistance? Use /support.",
        parse_mode="Markdown"
    )
