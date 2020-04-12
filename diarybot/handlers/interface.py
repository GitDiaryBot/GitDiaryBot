from diarybot.events import DiaryEvent
from diarybot.core.recorder import TextRecorder
from diarybot.tenant_config import TenantConfig


class EventHandler:

    def handle_event(self, event: DiaryEvent) -> None:
        """Handle incoming event."""


class RecordingEventHandler(EventHandler):

    @classmethod
    def load(cls, tenant_config: TenantConfig, recorder: TextRecorder) -> 'RecordingEventHandler':
        """Return new instance of this event handler."""
