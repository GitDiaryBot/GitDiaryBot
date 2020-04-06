import attr
from telegram.ext import BaseFilter, Filters

from diarybot.events import DiaryEvent, TextReceived, LocationReceived, VoiceReceived, PhotoReceived
from diarybot.extractors.interface import EventExtractorInterface
from diarybot.extractors.text import TextEventExtractor
from diarybot.extractors.voice import VoiceEventExtractor
from diarybot.extractors.location import LocationEventExtractor
from diarybot.extractors.photo import PhotoEventExtractor


@attr.s(slots=True, frozen=True, auto_attribs=True)
class Skill:
    tg_filter: BaseFilter
    extractor: EventExtractorInterface
    event_class: DiaryEvent


SKILLS = [
    Skill(
        tg_filter=Filters.text,
        extractor=TextEventExtractor,
        event_class=TextReceived,
    ),
    Skill(
        tg_filter=Filters.location,
        extractor=LocationEventExtractor,
        event_class=LocationReceived,
    ),
    Skill(
        tg_filter=Filters.voice,
        extractor=VoiceEventExtractor,
        event_class=VoiceReceived,
    ),
    Skill(
        tg_filter=Filters.photo,
        extractor=PhotoEventExtractor,
        event_class=PhotoReceived,
    ),
]
