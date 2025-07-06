import os
import subprocess

from aiogram import Router, types

from services.rate_limiter import is_allowed
from services.transcription import transcribe_audio

router = Router()


def register_video_note_handler(bot, client):
    @router.message(lambda m: m.video_note is not None)
    async def handle_video_note(message: types.Message):
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

        file_id = message.video_note.file_id
        file_info = await bot.get_file(file_id)

        input_path = f"input_{message.message_id}.mp4"
        mp3_path = f"user_{message.from_user.id}_msg_{message.message_id}.mp3"

        processing_msg = await message.answer("🎧 Converting...")

        try:
            await bot.download_file(file_info.file_path, input_path)

            subprocess.run([
                "ffmpeg", "-y", "-i", input_path, "-vn", "-acodec", "libmp3lame", mp3_path
            ], check=True)

            text = transcribe_audio(mp3_path, client)
            await processing_msg.edit_text(text)
        except Exception as e:
            await processing_msg.edit_text(f"Error: {e}")
        finally:
            os.remove(input_path)
            os.remove(mp3_path)

    return router
