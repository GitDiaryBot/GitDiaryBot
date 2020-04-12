from typing import Type

import attr
from telegram.ext import BaseFilter

from diarybot.events import DiaryEvent
from diarybot.extractors.interface import EventExtractorInterface
from diarybot.handlers.interface import EventHandler


@attr.s(slots=True, frozen=True, auto_attribs=True)
class Skill:
    tg_filter: BaseFilter
    extractor: Type[EventExtractorInterface]
    event_class: Type[DiaryEvent]
    event_handler_class: Type[EventHandler]
