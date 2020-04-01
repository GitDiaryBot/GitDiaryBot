from typing import Union

import attr


@attr.s(slots=True, frozen=True, auto_attribs=True)
class TextReceived:
    text: str


@attr.s(slots=True, frozen=True, auto_attribs=True)
class LocationReceived:
    latitude: float
    longitude: float


@attr.s(slots=True, frozen=True, auto_attribs=True)
class VoiceReceived:
    file_id: str
    data: bytes


@attr.s(slots=True, frozen=True, auto_attribs=True)
class PhotoReceived:
    file_id: str
    data: bytes


EventReceived = Union[TextReceived, LocationReceived, VoiceReceived]
