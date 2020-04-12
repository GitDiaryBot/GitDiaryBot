from typing import Iterator, List
from telegram import Message

from diarybot.events import DiaryEvent
from diarybot.skill_interface import Skill
from diarybot.extractors.interface import EventExtractorInterface


class EventExtractor(EventExtractorInterface):

    def __init__(self, skills: List[Skill]) -> None:
        self._specific_extractors = [
            skill.extractor()
            for skill in skills
        ]

    def extract_events(self, message: Message) -> Iterator[DiaryEvent]:
        for extractor in self._specific_extractors:
            yield from extractor.extract_events(message)
