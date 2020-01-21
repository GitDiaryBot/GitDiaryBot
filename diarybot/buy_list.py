from .text_handler import TextHandler


class BuyList(TextHandler):
    _TRIGGERS = (
        "buy",
        "купить",
    )

    def __init__(self, file_path: str) -> None:
        self._file_path = file_path

    def handle_text(self, text: str) -> None:
        item = self._match(text)
        if item:
            self._append_item(item)

    def _match(self, text: str) -> str:
        parts = text.split(None, 1)
        if not parts:
            return None
        head = parts[0].lower()
        tail = parts[1].strip()
        for trigger in self._TRIGGERS:
            if head == trigger:
                return tail
        return None

    def _append_item(self, text: str) -> None:
        with open(self._file_path, "at") as fobj:
            fobj.write(f"* {text}\n")
