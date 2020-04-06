from diarybot.events import TextReceived
from diarybot.core.recorder import TextRecorder
from .interface import EventHandler


class TextEventHandler(EventHandler):
    def __init__(self, recorder: TextRecorder) -> None:
        self._recorder = recorder

    def handle_event(self, event: TextReceived) -> None:
        self._recorder.append_text(event.text)
