from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

LANGUAGES_PER_PAGE = 5


async def send_language_page(
        target: types.Message | types.CallbackQuery,
        page: int,
        locale: dict,
        LANGUAGE_LIST: list,
        LANGUAGES_PER_PAGE: int = 5,
):
    start = page * LANGUAGES_PER_PAGE
    end = start + LANGUAGES_PER_PAGE

    builder = InlineKeyboardBuilder()
    for code, label in LANGUAGE_LIST[start:end]:
        builder.row(
            types.InlineKeyboardButton(text=label, callback_data=f"set_lang:{code}")
        )

    nav_buttons = []
    if page > 0:
        nav_buttons.append(types.InlineKeyboardButton(text="⬅️",
                                                      callback_data=f"lang_page:{page - 1}"))
    if end < len(LANGUAGE_LIST):
        nav_buttons.append(types.InlineKeyboardButton(text="➡️",
                                                      callback_data=f"lang_page:{page + 1}"))
    if nav_buttons:
        builder.row(*nav_buttons)

    if isinstance(target, types.Message):
        await target.answer(locale["choose_language_prompt"], reply_markup=builder.as_markup())
    elif isinstance(target, types.CallbackQuery):
        await target.message.edit_text(locale["choose_language_prompt"],
                                       reply_markup=builder.as_markup())
        await target.answer()
