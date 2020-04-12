from typing import Type, Callable

from diarybot.events import DiaryEvent
from diarybot.handlers.interface import EventHandler


HANDLERS_REGISTRY = {}


Registrator = Callable[[Type[EventHandler]], Type[EventHandler]]


def register_handler(event_type: Type[DiaryEvent]) -> Registrator:
    def _register_event_handler(handler_class: Type[EventHandler]) -> Type[EventHandler]:
        HANDLERS_REGISTRY.get(event_type, []).append(handler_class)
        return handler_class
    return _register_event_handler
