from diarybot.events import PhotoReceived
from diarybot.core.recorder import TextRecorder
from diarybot.transformers.photo import PhotoTransformer
from .interface import EventHandler


class PhotoEventHandler(EventHandler):
    def __init__(self, recorder: TextRecorder, photo_transformer: PhotoTransformer) -> None:
        self._recorder = recorder
        self._photo_transformer = photo_transformer

    def handle_event(self, event: PhotoReceived) -> None:
        with self._photo_transformer.file_writer(event.file_id) as fobj:
            fobj.write(event.data)
        text = self._photo_transformer.handle_file_id(event.file_id)
        self._recorder.append_text(text)