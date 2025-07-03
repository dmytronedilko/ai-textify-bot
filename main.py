import os
import requests
import cloudconvert
from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters import Command
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

bot = Bot(token=os.getenv("TG_BOT_API_KEY"))
dp = Dispatcher()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
cloudconvert.configure(api_key=os.getenv("CLOUDCONVERT_API_KEY"))

router = Router()

dp.include_router(router)


async def start_command(message: types.Message):
    await message.answer("Hi! Send me a voice message to get started.")


router.message.register(start_command, Command("start"))


def convert_ogg_to_mp3_cloudconvert(input_path: str, output_path: str):
    job = cloudconvert.Job.create(payload={
        "tasks": {
            "import-file": {
                "operation": "import/upload"
            },
            "convert-file": {
                "operation": "convert",
                "input": "import-file",
                "input_format": "ogg",
                "output_format": "mp3",
                "audio_codec": "mp3"
            },
            "export-file": {
                "operation": "export/url",
                "input": "convert-file"
            }
        }
    })

    upload_task = [task for task in job["tasks"] if task["name"] == "import-file"][0]
    upload_url = upload_task["result"]["form"]["url"]
    upload_params = upload_task["result"]["form"]["parameters"]

    with open(input_path, 'rb') as f:
        files = {'file': (os.path.basename(input_path), f)}
        requests.post(upload_url, data=upload_params, files=files)

    job = cloudconvert.Job.wait(id=job["id"])

    export_task = [task for task in job["tasks"] if task["name"] == "export-file"][0]
    file_url = export_task["result"]["files"][0]["url"]

    response = requests.get(file_url)
    with open(output_path, 'wb') as out_file:
        out_file.write(response.content)


@dp.message(lambda message: message.voice is not None)
async def handle_voice(message: types.Message):
    file_id = message.voice.file_id
    file_info = await bot.get_file(file_id)

    ogg_path = f"voice_{message.message_id}.ogg"
    mp3_path = f"voice_{message.message_id}.mp3"

    await bot.download_file(file_info.file_path, ogg_path)
    await message.answer("Converting...")

    try:
        convert_ogg_to_mp3_cloudconvert(ogg_path, mp3_path)
    except Exception as e:
        await message.reply(f"Conversion error: {e}")
        return

    try:
        with open(mp3_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model="gpt-4o-transcribe",
                file=audio_file,
                language="en"
            )
            await message.reply(f"{transcription.text}")
    except Exception as e:
        await message.reply(f"Transcription error: {e}")

    os.remove(ogg_path)
    os.remove(mp3_path)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
