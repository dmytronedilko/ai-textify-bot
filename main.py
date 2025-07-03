import os
from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters import Command
from dotenv import load_dotenv
from openai import OpenAI
from pydub import AudioSegment

load_dotenv()

bot = Bot(token=os.getenv("TG_BOT_API_KEY"))
dp = Dispatcher()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

router = Router()
dp.include_router(router)


async def start_command(message: types.Message):
    await message.answer("Hi! Send me a voice message to get started.")


router.message.register(start_command, Command("start"))


@dp.message(lambda message: message.voice is not None)
async def handle_voice(message: types.Message):
    file_id = message.voice.file_id
    file_info = await bot.get_file(file_id)

    ogg_path = f"voice_{message.message_id}.ogg"
    mp3_path = f"user_{message.from_user.id}_msg_{message.message_id}.mp3"

    await bot.download_file(file_info.file_path, ogg_path)
    await message.answer("Converting...")

    try:
        audio = AudioSegment.from_file(file=ogg_path, format="ogg")
        audio.export(out_f=mp3_path, format="mp3")
    except Exception as e:
        await message.reply(f"Conversion error: {e}")
        return

    try:
        with open(mp3_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
            text = transcription.text

            await message.reply(f"{text}")
    except Exception as e:
        await message.reply(f"Transcription error: {e}")

    os.remove(ogg_path)
    os.remove(mp3_path)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
