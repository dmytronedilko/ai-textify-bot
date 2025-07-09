import json
from pathlib import Path
from sqlalchemy import select
from database.db import get_db
from database.models import User
from services.redis_client import redis_client

DEFAULT_LANG = "en"


async def get_user_locale(user_id: int) -> dict:
    lang_code = await redis_client.get(f"user_lang:{user_id}")

    if not lang_code:
        db = next(get_db())
        user = db.execute(select(User).where(User.user_id == user_id)).scalar_one_or_none()
        if user:
            lang_code = user.language
            await redis_client.set(f"user_lang:{user_id}", lang_code, ex=10800)
        else:
            lang_code = DEFAULT_LANG

    path = Path("locales") / f"{lang_code}.json"
    if not path.exists():
        path = Path("locales") / f"{DEFAULT_LANG}.json"

    with open(path, encoding="utf-8") as f:
        return json.load(f)
