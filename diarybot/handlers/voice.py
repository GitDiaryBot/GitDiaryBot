from diarybot.events import VoiceReceived
from diarybot.core.recorder import TextRecorder
from diarybot.transformers.voice import VoiceTransformer
from .interface import EventHandler


class VoiceEventHandler(EventHandler):
    def __init__(self, recorder: TextRecorder, voice_transformer: VoiceTransformer) -> None:
        self._recorder = recorder
        self._voice_transformer = voice_transformer

    def handle_event(self, event: VoiceReceived) -> None:
        with self._voice_transformer.file_writer(event.file_id) as fobj:
            fobj.write(event.data)
        message = self._voice_transformer.handle_file_id(event.file_id)
        self._recorder.append_text(text=message)
