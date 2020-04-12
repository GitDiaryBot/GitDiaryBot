import abc
from diarybot.events import DiaryEvent


class TenantInterface(abc.ABC):
    @abc.abstractmethod
    def handle_event(self, event: DiaryEvent) -> None:
        """Handle incoming chat event."""
