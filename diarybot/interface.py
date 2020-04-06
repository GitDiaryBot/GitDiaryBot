import abc
from diarybot.events import EventReceived


class TenantInterface(abc.ABC):
    @abc.abstractmethod
    def handle_event(self, event: EventReceived) -> None:
        """Handle incoming chat event."""
