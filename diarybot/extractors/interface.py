import abc
from typing import Iterator
from telegram import Message

from diarybot.events import EventReceived


class EventExtractorInterface(abc.ABC):
    @abc.abstractmethod
    def extract_events(self, message: Message) -> Iterator[EventReceived]:
        """Extract events from incoming message."""
