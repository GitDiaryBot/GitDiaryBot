"""Append new diary records to a text file, commit and push to git repo."""

import logging
from typing import Callable, List

import attr


logger = logging.getLogger(__name__)


@attr.s(slots=True, frozen=True, auto_attribs=True)
class TextRecorder:
    """Text recording orchestration through callbacks."""

    before_write: List[Callable]
    on_write: List[Callable]
    after_write: List[Callable]

    def append_text(self, text: str) -> None:
        """Append text message and push it to remote upstream."""
        for callback in self.before_write:
            callback()
        for callback in self.on_write:
            callback(text)
        for callback in self.after_write:
            callback()
