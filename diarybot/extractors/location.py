from typing import Iterator
from telegram import Message

from diarybot.events import LocationReceived
from .interface import EventExtractorInterface


class LocationEventExtractor(EventExtractorInterface):
    def extract_events(self, message: Message) -> Iterator[LocationReceived]:
        if message.location:
            yield LocationReceived(
                message.location.latitude, message.location.longitude
            )
