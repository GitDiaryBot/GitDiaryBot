from diarybot.events import LocationReceived
from diarybot.core.recorder import TextRecorder
from diarybot.transformers.location import LocationTransformer
from .interface import EventHandler


class LocationEventHandler(EventHandler):
    def __init__(self, recorder: TextRecorder, location_transformer: LocationTransformer) -> None:
        self._recorder = recorder
        self._location_transformer = location_transformer

    def handle_event(self, event: LocationReceived) -> None:
        text = self._location_transformer.handle_coordinates(
            event.latitude, event.longitude
        )
        self._recorder.append_text(text=text)
