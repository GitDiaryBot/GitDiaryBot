from typing import Union

import attr


def event(func):
    return attr.s(slots=True, frozen=True, auto_attribs=True)(func)


@event
class DiaryEvent:
    pass


@event
class TextReceived(DiaryEvent):
    text: str


@event
class LocationReceived(DiaryEvent):
    latitude: float
    longitude: float


@event
class VoiceReceived(DiaryEvent):
    file_id: str
    data: bytes


@event
class PhotoReceived(DiaryEvent):
    file_id: str
    data: bytes
