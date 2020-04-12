import os
from typing import Optional

from diarybot.core.speech_to_text import SpeechToTextClient
from .base_media import BaseMediaTransformer


_TRANSCRIPT_LANGUAGE_CODES = ("ru-RU", "en-US")
_AUDIO_DIR = 'audio'


class VoiceTransformer(BaseMediaTransformer):

    _FILE_NAME_PTRN = '{}.ogg'

    def __init__(self,
                 speech_to_text: Optional[SpeechToTextClient],
                 base_dir: str,
                 rel_dir: str = _AUDIO_DIR) -> None:
        super().__init__(base_dir, rel_dir)
        self._speech_to_text = speech_to_text

    def handle_file_id(self, file_id: str) -> str:
        rel_path = self._rel_path(file_id)
        abs_path = os.path.join(self._base_dir, rel_path)
        message = f"Audio: {rel_path}"
        if self._speech_to_text:
            text = self._transcipt(abs_path)
            if text:
                message += f"\n{text}"
        return message

    def _transcipt(self, file_path: str) -> str:
        with open(file_path, "rb") as fobj:
            audio = fobj.read()
        for language_code in _TRANSCRIPT_LANGUAGE_CODES:
            text = self._speech_to_text(language_code, audio)
            if text:
                return text
        return ""
