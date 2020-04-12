from typing import Iterator
from telegram import Message

from diarybot.events import DiaryEvent


class EventExtractorInterface:

    def extract_events(self, message: Message) -> Iterator[DiaryEvent]:
        """Extract events from incoming message."""
        # pylint: disable=no-self-use
        del message
        yield DiaryEvent()
