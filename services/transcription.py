from pydub import AudioSegment


def convert_ogg_to_mp3(ogg_path: str, mp3_path: str):
    audio = AudioSegment.from_file(file=ogg_path, format="ogg")
    audio.export(out_f=mp3_path, format="mp3")


def transcribe_audio(mp3_path: str, client):
    try:
        with open(mp3_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
        return transcription.text
    except Exception as e:
        return f"[Transcription error: {e}]"