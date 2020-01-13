import os

from diarybot.speech_to_text import SpeechToTextClient


HERE = os.path.dirname(__file__)
GOOGLE_API_KEY = os.environ['DIARY_GOOGLE_API_KEY']


def test_english():
    file_path = os.path.join(HERE, 'assets', 'en_sample.ogg')
    client = SpeechToTextClient(GOOGLE_API_KEY)
    with open(file_path, "rb") as fobj:
        audio = fobj.read()
    text = client.transcript("en-US", audio)
    assert text == "Text to speech test."


def test_russian():
    file_path = os.path.join(HERE, 'assets', 'ru_sample.ogg')
    client = SpeechToTextClient(GOOGLE_API_KEY)
    with open(file_path, "rb") as fobj:
        audio = fobj.read()
    text = client.transcript("ru-RU", audio)
    assert text == "проверка распознавание"
