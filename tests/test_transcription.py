import os
import unittest
from fuzzywuzzy import fuzz
from services.transcription import transcribe_audio
from bot.setup import client
import re


def normalize(text):
    return re.sub(r'\W+', ' ', text).lower().strip()


class TestTranscription(unittest.TestCase):
    def test_audio_transcription(self):
        audio_relative_path = "mocks/test_audio/test_01_20s.wav"
        audio_absolute_path = os.path.abspath(audio_relative_path)

        expected = '''
                Dancing in the masquerade,
                idle truth and plain sight jaded, pop, roll, click, shot,
                who will I be today or not?
                But such a tide as moving seems asleep, 
                too full for sound and foam, when that witch
                drew from out the boundless deep turns again home, 
                twilight and evening bell and after
                that
                '''

        actual = transcribe_audio(audio_absolute_path, client)

        similarity = fuzz.ratio(normalize(expected), normalize(actual))

        self.assertGreaterEqual(similarity, 95,
                                f"Text similarity too low: {similarity}%\nActual:\n{actual}\nExpected:\n{expected}")

        print(f"Text similarity: {similarity}%\nActual:\n{actual}\nExpected:\n{expected}")

    def test_video_transcription(self):
        video_relative_path = "mocks/test_video/test_01_30s.mp4"
        video_absolute_path = os.path.abspath(video_relative_path)

        expected = '''
                Hey there, this is a quick and silly video to allow you to experiment
                a little bit with the process of transcription on YouTube. 
                Also I'm looking for you to do here is to use the YouTube tool to 
                transcribe this message and then click sync and set the timing so 
                you can get a quick idea about how the whole process works. 
                Well, this wraps up the video, good luck and I will talk to you about
                it soon.
                '''

        actual = transcribe_audio(video_absolute_path, client)

        similarity = fuzz.ratio(normalize(expected), normalize(actual))

        self.assertGreaterEqual(similarity, 95,
                                f"Text similarity too low: {similarity}%\nActual:\n{actual}\nExpected:\n{expected}")
        print(f"Text similarity: {similarity}%\nActual:\n{actual}\nExpected:\n{expected}")

if __name__ == '__main__':
    unittest.main()
