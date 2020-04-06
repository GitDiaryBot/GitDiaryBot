import os
from contextlib import contextmanager
from typing import Iterator, Optional, BinaryIO

from diarybot.core.speech_to_text import SpeechToTextClient


_TRANSCRIPT_LANGUAGE_CODES = ("ru-RU", "en-US")
_AUDIO_DIR = 'audio'


class VoiceTransformer:

    _FILE_NAME_PTRN = '{}.ogg'

    def __init__(self,
                 speech_to_text: Optional[SpeechToTextClient],
                 base_dir: str,
                 rel_dir: str = _AUDIO_DIR) -> None:
        self._speech_to_text = speech_to_text
        self._base_dir = base_dir
        self._rel_dir = rel_dir
        self._target_dir = os.path.join(base_dir, rel_dir)

    @contextmanager
    def file_writer(self, file_id: str) -> Iterator[BinaryIO]:
        if not os.path.exists(self._target_dir):
            os.makedirs(self._target_dir)
        abs_path = os.path.join(self._target_dir, self._FILE_NAME_PTRN.format(file_id))
        with open(abs_path, "wb") as fobj:
            yield fobj

    def handle_file_id(self, file_id: str) -> str:
        rel_path = os.path.join(self._rel_dir, self._FILE_NAME_PTRN.format(file_id))
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
