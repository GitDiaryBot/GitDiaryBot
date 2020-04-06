from typing import Iterator
from telegram import Message

from diarybot.events import TextReceived
from .interface import EventExtractorInterface


class TextEventExtractor(EventExtractorInterface):
    def extract_events(self, message: Message) -> Iterator[TextReceived]:
        if message.text:
            yield TextReceived(text=message.text)
