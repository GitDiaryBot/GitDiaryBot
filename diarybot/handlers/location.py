from diarybot.events import LocationReceived
from diarybot.core.recorder import TextRecorder
from diarybot.transformers.location import LocationTransformer
from diarybot.tenant_config import TenantConfig
from .interface import RecordingEventHandler
from .registry import register_handler


@register_handler(LocationReceived)
class LocationEventHandler(RecordingEventHandler):
    def __init__(self, recorder: TextRecorder, location_transformer: LocationTransformer) -> None:
        self._recorder = recorder
        self._location_transformer = location_transformer

    def handle_event(self, event: LocationReceived) -> None:
        text = self._location_transformer.handle_coordinates(
            event.latitude, event.longitude
        )
        self._recorder.append_text(text=text)

    @classmethod
    def load(cls, tenant_config: TenantConfig, recorder: TextRecorder) -> 'LocationEventHandler':
        location_transformer = (
            LocationTransformer(tenant_config.google_api_key)
            if tenant_config.google_api_key
            else None
        )
        return cls(
            recorder=recorder,
            location_transformer=location_transformer,
        )
