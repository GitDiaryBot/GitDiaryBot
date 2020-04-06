from diarybot.events import EventReceived


class EventHandler:

    def handle_event(self, event: EventReceived) -> None:
        """Handle incoming event."""
