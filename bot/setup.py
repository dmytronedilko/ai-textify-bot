import os
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from openai import OpenAI

from bot.commands import start, support
from bot.handlers.textify_handler import register_textify_handler
from bot.handlers.video_note_handler import register_video_note_handler
from bot.handlers.voice_handler import register_voice_handler

load_dotenv()

bot = Bot(token=os.getenv("TG_BOT_API_KEY"))
dp = Dispatcher()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

dp.include_router(start.router)
dp.include_router(support.router)
dp.include_router(register_voice_handler(bot, client))
dp.include_router(register_video_note_handler(bot, client))
dp.include_router(register_textify_handler(bot, client))
