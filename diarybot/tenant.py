from typing import Dict, Type

import attr
import git

from diarybot.interface import TenantInterface
from diarybot.handlers.interface import EventHandler
from .events import EventReceived


@attr.s(slots=True, frozen=True, auto_attribs=True)
class Tenant(TenantInterface):
    """Tenant-specific collection of objects."""
    def __init__(self, handlers: Dict[Type, EventHandler]) -> None:
        self._handlers = handlers

    def handle_event(self, event: EventReceived) -> None:
        handler = self._handlers[type(event)]
        handler(event)

    @classmethod
    def install_repo_url(cls, diary_dir: str, repo_url: str) -> None:
        git.Repo.clone_from(repo_url, diary_dir)
