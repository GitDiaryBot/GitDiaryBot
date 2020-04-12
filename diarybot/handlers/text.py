from diarybot.events import TextReceived
from diarybot.core.recorder import TextRecorder
from diarybot.tenant_config import TenantConfig
from .interface import RecordingEventHandler
from .registry import register_handler


@register_handler(TextReceived)
class TextEventHandler(RecordingEventHandler):
    def __init__(self, recorder: TextRecorder) -> None:
        self._recorder = recorder

    def handle_event(self, event: TextReceived) -> None:
        self._recorder.append_text(event.text)

    @classmethod
    def load(cls, tenant_config: TenantConfig, recorder: TextRecorder) -> 'TextEventHandler':
        del tenant_config  # recorder already bound to the tenant
        return cls(recorder=recorder)
