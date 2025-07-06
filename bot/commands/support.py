from aiogram import Router, types
from aiogram.filters import Command

router = Router()


@router.message(Command("support"))
async def support_command(message: types.Message):
    await message.answer(
        "🔧 <b>Support</b>\n\n"
        "If you have any questions, run into issues, or want "
        "to share suggestions — we’re here to help!\n\n"
        "📨 <b>Contact us:</b> <a href=\"https://forms.gle/9tTL4i23c6MMF5eo7\">"
        "Support Form</a>\n"
        "🛠 <b>Support hours:</b> Mon–Fri, 10:00–19:00 (UTC+3)\n\n"
        "Thank you for using our bot! 💙",
        parse_mode="HTML"
    )
