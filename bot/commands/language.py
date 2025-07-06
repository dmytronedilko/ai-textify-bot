from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()

LANGUAGE_OPTIONS = {
    "en": "🇺🇸 English",
    "uk": "🇺🇦 Українська",
}


@router.message(Command("language"))
async def language_command(message: types.Message):
    builder = InlineKeyboardBuilder()
    for code, label in LANGUAGE_OPTIONS.items():
        builder.button(text=label, callback_data=f"set_lang:{code}")
    await message.answer("Please choose your language:", reply_markup=builder.as_markup())


@router.callback_query(F.data.startswith("set_lang:"))
async def handle_language_choice(callback: types.CallbackQuery):
    lang_code = callback.data.split(":")[1]
    await callback.message.edit_text(
        f"✅ Language set "
        f"to: {LANGUAGE_OPTIONS.get(lang_code, lang_code)}"
    )
    await callback.answer()
