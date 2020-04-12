from diarybot.events import VoiceReceived
from diarybot.core.recorder import TextRecorder
from diarybot.core.speech_to_text import SpeechToTextClient
from diarybot.transformers.voice import VoiceTransformer
from diarybot.tenant_config import TenantConfig
from .interface import RecordingEventHandler


class VoiceEventHandler(RecordingEventHandler):
    def __init__(self, recorder: TextRecorder, voice_transformer: VoiceTransformer) -> None:
        self._recorder = recorder
        self._voice_transformer = voice_transformer

    def handle_event(self, event: VoiceReceived) -> None:
        with self._voice_transformer.file_writer(event.file_id) as fobj:
            fobj.write(event.data)
        message = self._voice_transformer.handle_file_id(event.file_id)
        self._recorder.append_text(text=message)

    @classmethod
    def load(cls, tenant_config: TenantConfig, recorder: TextRecorder) -> 'VoiceEventHandler':
        speech_to_text = (
            SpeechToTextClient(google_api_key=tenant_config.google_api_key)
            if tenant_config.google_api_key
            else None
        )
        return VoiceEventHandler(
            recorder=recorder,
            voice_transformer=VoiceTransformer(
                base_dir=tenant_config.base_dir,
                speech_to_text=speech_to_text,
            ),
        )
