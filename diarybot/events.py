from typing import Union

import attr


@attr.s(slots=True, frozen=True, auto_attribs=True)
class DiaryEvent:
    pass


class TextReceived(DiaryEvent):
    text: str


class LocationReceived(DiaryEvent):
    latitude: float
    longitude: float


class VoiceReceived(DiaryEvent):
    file_id: str
    data: bytes


class PhotoReceived(DiaryEvent):
    file_id: str
    data: bytes


EventReceived = Union[TextReceived, LocationReceived, VoiceReceived]
