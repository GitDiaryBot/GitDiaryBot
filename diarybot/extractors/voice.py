from typing import Iterator
from io import BytesIO

from telegram import Message

from diarybot.events import VoiceReceived
from .interface import EventExtractorInterface


class VoiceEventExtractor(EventExtractorInterface):
    def extract_events(self, message: Message) -> Iterator[VoiceReceived]:
        if message.voice:
            fobj = BytesIO()
            tg_file = message.voice.get_file()
            tg_file.download(out=fobj)
            yield VoiceReceived(tg_file.file_id, fobj.getvalue())
