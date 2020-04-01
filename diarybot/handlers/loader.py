from typing import List

from .interface import EventSpec
from .text_spec import build_text_event_spec


def load_specs() -> List[EventSpec]:
    return [
        build_text_event_spec(),
    ]
