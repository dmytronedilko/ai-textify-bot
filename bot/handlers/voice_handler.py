import os
from aiogram import Router, types
from services.transcription import convert_ogg_to_mp3, transcribe_audio

router = Router()

def register_voice_handler(bot, client):
    @router.message(lambda m: m.voice is not None)
    async def handle_voice(message: types.Message):
        file_id = message.voice.file_id
        file_info = await bot.get_file(file_id)

        ogg_path = f"voice_{message.message_id}.ogg"
        mp3_path = f"user_{message.from_user.id}_msg_{message.message_id}.mp3"

        await bot.download_file(file_info.file_path, ogg_path)
        await message.answer("Converting...")

        try:
            convert_ogg_to_mp3(ogg_path, mp3_path)
            text = transcribe_audio(mp3_path, client)
            await message.reply(text)
        except Exception as e:
            await message.reply(f"Error: {e}")
        finally:
            os.remove(ogg_path)
            os.remove(mp3_path)

    return router
