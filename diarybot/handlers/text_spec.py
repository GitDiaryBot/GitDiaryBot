from typing import Iterable

from telegram import Message
from telegram.ext.filters import Filters

from diarybot.events import TextReceived
from diarybot.recorder import TextRecorder
from diarybot.tenant import Tenant
from .interface import EventExtractor, EventHandler, EventSpec


class TextEventExtractor(EventExtractor):
    def extract_events(self, message: Message) -> Iterable[TextReceived]:
        if message.text:
            yield TextReceived(message.text)

    __call__ = extract_events


class TextEventHandler(EventHandler):
    recorder: TextRecorder

    def __init__(self, tenant: Tenant) -> None:
        self._tenant = tenant

    def handle_event(self, event: TextReceived) -> None:
        self._tenant.recorder.append_text(event.text)


def build_text_event_spec() -> EventSpec:
    return EventSpec(
        event_filter=Filters.text,
        extractor=TextEventExtractor(),
        handler_class=TextEventHandler,
        event_class=TextReceived,
    )
