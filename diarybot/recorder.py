"""Append new diary records to a text file, commit and push to git repo."""

import os
import io
import datetime
import logging
from contextlib import contextmanager
from typing import Callable, List, Iterable

import git
import tzlocal
import requests

from .text_handler import TextHandler
from .speech_to_text import SpeechToTextClient


logger = logging.getLogger(__name__)


_RECORD_PTRN = """
{time}

{text}
"""
_TIME_FORMAT = '%Y/%m/%d %H:%M:%S %Z %z'
_COMMIT_MESSAGE = 'add record from GitDiaryBot'
_LOCATION_FORMAT = "Latitude: {latitude}\nLongitude: {longitude}"
_GEOCODING_API = (
    "https://maps.googleapis.com/maps/api/geocode/json"
)
_TRANSCRIPT_LANGUAGE_CODES = ("ru-RU", "en-US")
_AUDIO_DIR = 'audio'


class GitSync:
    """Directory synchronization using Git repository."""

    def __init__(self, git_dir: str, repo_class: Callable = git.Repo) -> None:
        self._repo = repo_class(git_dir)

    def on_before_write(self):
        """Download remote changes."""
        self._repo.remotes[0].pull()

    def on_after_write(self):
        """Upload local changes."""
        self._repo.git.add(A=True)
        self._repo.index.commit(_COMMIT_MESSAGE)
        self._repo.remotes[0].push()


class GitRecorder:  # pylint: disable=too-many-instance-attributes
    """Plain text diary storage."""

    def __init__(  # pylint: disable=too-many-arguments
            self,
            git_dir: str,
            diary_file_name: str,
            google_api_key: str = None,
            text_formatter: Callable = None,
            extra_text_handlers: List[TextHandler] = None,
            speech_to_text: SpeechToTextClient = None,
    ) -> None:
        self._diary_file_name = diary_file_name
        self._git_dir = git_dir
        self._diary_file_path = os.path.join(git_dir, diary_file_name)
        self._format = text_formatter or naive_format
        self._google_api_key = google_api_key
        self._text_handlers = extra_text_handlers or []
        self._speech_to_text = speech_to_text
        self.before_write = []
        self.after_write = []

    def append_text(self, text: str) -> None:
        """Append text message and push it to remote upstream."""
        for callback in self.before_write:
            callback()
        self._write_text(text)
        for callback in self.after_write:
            callback()

    def append_location(self, latitude: float, longitude: float) -> None:
        latlon = _LOCATION_FORMAT.format(
            latitude=latitude,
            longitude=longitude,
        )
        if self._google_api_key:
            address = self._resolve_address(latitude, longitude)
            if address:
                message = f"{latlon}\nAddress: {address}"
        else:
            message = latlon
        self.append_text(message)

    @contextmanager
    def append_audio(self, audio_id) -> Iterable[io.BufferedWriter]:
        audio_dir = os.path.join(self._git_dir, _AUDIO_DIR)
        if not os.path.exists(audio_dir):
            os.makedirs(audio_dir)
        rel_path = os.path.join(_AUDIO_DIR, f"{audio_id}.ogg")
        abs_path = os.path.join(self._git_dir, rel_path)
        with open(abs_path, "wb") as fobj:
            yield fobj
        message = f"Audio: {rel_path}"
        if self._google_api_key and self._speech_to_text:
            text = self._transcipt(abs_path)
            if text:
                message += f"\n{text}"
        self.append_text(message)

    def _transcipt(self, file_path: str) -> str:
        with open(file_path, "rb") as fobj:
            audio = fobj.read()
        for language_code in _TRANSCRIPT_LANGUAGE_CODES:
            text = self._speech_to_text(language_code, audio)
            if text:
                return text
        return ""

    def _resolve_address(self, latitude: float, longitude: float) -> str:
        try:
            response = requests.get(
                _GEOCODING_API,
                {
                    "latlng": f"{latitude},{longitude}",
                    "key": self._google_api_key,
                }
            )
            response.raise_for_status()
            results = response.json().get('results')
            if results:
                return results[0]['formatted_address']
        except requests.RequestException:
            logger.exception("Failed to resolve address.")
        return ""

    def _write_text(self, text: str) -> None:
        # TODO: make time zone configurable
        now = datetime.datetime.now(tzlocal.get_localzone())
        record = self._format(now, text)
        with open(self._diary_file_path, "at") as fobj:
            fobj.write(record)
        for handler in self._text_handlers:
            handler.handle_text(text)


def naive_format(time: datetime.datetime, text: str) -> str:
    return _RECORD_PTRN.format(
        time=time.strftime(_TIME_FORMAT),
        text=text.strip(),
    )
