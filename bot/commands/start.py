from aiogram import Router, types
from aiogram.filters import Command
from sqlalchemy.orm import Session
from database.db import get_db
from database.models import User
from services.get_user_locale import get_user_locale
from services.redis_client import redis_client

router = Router()


@router.message(Command("start"))
async def start_command(message: types.Message):
    db_gen = get_db()
    db: Session = next(db_gen)
    try:
        user = db.query(User).filter_by(user_id=message.from_user.id).first()

        if not user:
            user = User(user_id=message.from_user.id, language="en")
            db.add(user)
            db.commit()
            await redis_client.set(f"user_lang:{user.user_id}", "en", ex=10800)

        locale = await get_user_locale(message.from_user.id)

        await message.answer(locale["welcome_message"], parse_mode="Markdown")
    finally:
        try:
            next(db_gen)
        except StopIteration:
            pass
