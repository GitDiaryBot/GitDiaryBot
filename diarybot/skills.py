from telegram.ext import Filters

from diarybot.events import TextReceived, LocationReceived, VoiceReceived, PhotoReceived
from diarybot.extractors.location import LocationEventExtractor
from diarybot.extractors.photo import PhotoEventExtractor
from diarybot.extractors.text import TextEventExtractor
from diarybot.extractors.voice import VoiceEventExtractor
from diarybot.handlers.location import LocationEventHandler
from diarybot.handlers.photo import PhotoEventHandler
from diarybot.handlers.text import TextEventHandler
from diarybot.handlers.voice import VoiceEventHandler
from diarybot.skill_interface import Skill


SKILLS = [
    Skill(
        tg_filter=Filters.text,
        extractor=TextEventExtractor,
        event_class=TextReceived,
        event_handler_class=TextEventHandler,
    ),
    Skill(
        tg_filter=Filters.location,
        extractor=LocationEventExtractor,
        event_class=LocationReceived,
        event_handler_class=LocationEventHandler,
    ),
    Skill(
        tg_filter=Filters.voice,
        extractor=VoiceEventExtractor,
        event_class=VoiceReceived,
        event_handler_class=VoiceEventHandler,
    ),
    Skill(
        tg_filter=Filters.photo,
        extractor=PhotoEventExtractor,
        event_class=PhotoReceived,
        event_handler_class=PhotoEventHandler,
    ),
]
