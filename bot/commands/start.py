from aiogram import Router, types
from aiogram.filters import Command
from sqlalchemy.orm import Session
from database.db import get_db
from database.models import User

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

        await message.answer(
            "👋 Welcome to Textify!\n\n"
            "🎤 Just send a voice message — I’ll transcribe it for you.\n"
            "📌 In groups, use the /textify command to transcribe replies.\n\n"
            "❓ Need assistance? Use /support.",
            parse_mode="Markdown"
        )
    finally:
        db_gen.close()