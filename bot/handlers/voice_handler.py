import os
from aiogram import Router, types

from services.rate_limiter import is_allowed
from services.transcription import convert_ogg_to_mp3, transcribe_audio

router = Router()


def register_voice_handler(bot, client):
    @router.message(lambda m: m.voice is not None)
    async def handle_voice(message: types.Message):
        user_id = message.from_user.id

        if not await is_allowed(user_id):
            await message.reply(
                f"❌ You’ve reached the weekly limit of "
                f"{os.getenv('WEEKLY_LIMIT', 10)} voice or video messages.\n\n"
                f"🚀 To unlock <b>unlimited</b> access to the bot, "
                f"upgrade to Premium using the /premium command.",
                parse_mode="HTML"
            )
            return

        file_id = message.voice.file_id
        file_info = await bot.get_file(file_id)

        ogg_path = f"voice_{message.message_id}.ogg"
        mp3_path = f"user_{message.from_user.id}_msg_{message.message_id}.mp3"

        processing_msg = await message.answer("Converting...")

        try:
            await bot.download_file(file_info.file_path, ogg_path)

            convert_ogg_to_mp3(ogg_path, mp3_path)
            text = transcribe_audio(mp3_path, client)
            await processing_msg.edit_text(text)
        except Exception as e:
            await processing_msg.edit_text(f"Error: {e}")
        finally:
            os.remove(ogg_path)
            os.remove(mp3_path)

    return router
