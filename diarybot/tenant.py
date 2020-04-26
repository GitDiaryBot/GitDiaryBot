from typing import Dict, Type

from diarybot.interface import TenantInterface
from diarybot.handlers.interface import EventHandler
from .events import DiaryEvent


class Tenant(TenantInterface):
    """Tenant-specific collection of objects."""
    def __init__(self, handlers: Dict[Type[DiaryEvent], EventHandler]) -> None:
        self._handlers = handlers

    def handle_event(self, event: DiaryEvent) -> None:
        handler = self._handlers[type(event)]
        handler.handle_event(event)
