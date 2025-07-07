from aiogram import Router, types, F
from aiogram.filters import Command
from sqlalchemy import select
from database.models import User
from database.db import get_db
from services.get_user_locale import get_user_locale
from services.redis_client import redis_client
from services.send_language_page import send_language_page

router = Router()

LANGUAGE_LIST = [
    ("en", "🇺🇸 English"),
    ("uk", "🇺🇦 Українська"),
    ("es", "🇪🇸 Español"),
    ("de", "🇩🇪 Deutsch"),
    ("fr", "🇫🇷 Français"),
    ("it", "🇮🇹 Italiano"),
    ("pl", "🇵🇱 Polski"),
    ("ro", "🇷🇴 Română"),
    ("bg", "🇧🇬 Българська"),
    ("sv", "🇸🇪 Svenska")
]

LANGUAGES_PER_PAGE = 5


@router.message(Command("language"))
async def language_command(message: types.Message):
    locale = await get_user_locale(message.from_user.id)
    await send_language_page(
        message,
        page=0,
        locale=locale,
        LANGUAGE_LIST=LANGUAGE_LIST,
        LANGUAGES_PER_PAGE=LANGUAGES_PER_PAGE
    )


@router.callback_query(F.data.startswith("lang_page:"))
async def change_language_page(callback: types.CallbackQuery):
    page = int(callback.data.split(":")[1])
    locale = await get_user_locale(callback.from_user.id)
    await send_language_page(
        callback,
        page=page,
        locale=locale,
        LANGUAGE_LIST=LANGUAGE_LIST,
        LANGUAGES_PER_PAGE=LANGUAGES_PER_PAGE
    )


@router.callback_query(F.data.startswith("set_lang:"))
async def handle_language_choice(callback: types.CallbackQuery):
    lang_code = callback.data.split(":")[1]

    db = next(get_db())
    user = db.execute(select(User)
                      .where(User.user_id == callback.from_user.id)).scalar_one_or_none()

    if user is None:
        user = User(user_id=callback.from_user.id, language=lang_code)
        db.add(user)
    else:
        user.language = lang_code

    db.commit()
    await redis_client.set(f"user_lang:{user.user_id}", lang_code, ex=10800)

    locale = await get_user_locale(callback.from_user.id)
    await callback.message.edit_text(
        locale["language_set_confirmation"].format(
            language=dict(LANGUAGE_LIST).get(lang_code, lang_code)
        )
    )
    await callback.answer()
