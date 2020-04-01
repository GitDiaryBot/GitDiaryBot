from typing import Iterable, Type

import attr
from telegram import Message
from telegram.ext.filters import BaseFilter

from diarybot.events import EventReceived


class EventExtractor:
    def extract_events(self, message: Message) -> Iterable[EventReceived]:
        """Extract events from incoming message."""


class EventHandler:
    def handle_event(self, event: EventReceived) -> None:
        """Handle incoming event."""


@attr.s(slots=True, frozen=True, auto_attribs=True)
class EventSpec:
    event_filter: BaseFilter
    extractor: EventExtractor
    handler_class: Type
    event_class: Type

    def attach(self, bot: Updater) -> None:
        bot.dispatcher.add_handler(MessageHandler(
            filters=self.event_filter,
            callback=self._on_event,
        ))

    def _on_event(self, message: Message) -> None:
        for event in self.extractor(message):
            self.handler_class()

