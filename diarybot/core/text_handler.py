class TextHandler:

    def handle_text(self, text: str) -> None:
        raise NotImplementedError

    def __call__(self, text: str) -> None:
        # Callback-like short hand
        return self.handle_text(text)
