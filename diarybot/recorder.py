"""Append new diary records to a text file, commit and push to git repo."""

import os
import datetime
import logging
from typing import Callable

import git
import tzlocal
import requests


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


class GitRecorder:
    """Git repo plain text diary storage."""

    def __init__(  # pylint: disable=too-many-arguments
            self,
            git_dir: str,
            diary_file_name: str,
            geolocation_api_key: str = None,
            repo_class: Callable = git.Repo,
            text_formatter: Callable = None,
    ) -> None:
        self._diary_file_name = diary_file_name
        self._repo = repo_class(git_dir)
        self._diary_file_path = os.path.join(git_dir, diary_file_name)
        self._format = text_formatter or naive_format
        self._geolocation_api_key = geolocation_api_key

    def append_text(self, text: str) -> None:
        """Append text message and push it to remote upstream."""
        # TODO: make time zone configurable
        now = datetime.datetime.now(tzlocal.get_localzone())
        self._repo.remotes[0].pull()
        record = self._format(now, text)
        self._write_record(record)
        self._repo.index.add(self._diary_file_name)
        self._repo.index.commit(_COMMIT_MESSAGE)
        self._repo.remotes[0].push()

    def append_location(self, latitude: float, longitude: float) -> None:
        latlon = _LOCATION_FORMAT.format(
            latitude=latitude,
            longitude=longitude,
        )
        if self._geolocation_api_key:
            address = self._resolve_address(latitude, longitude)
            if address:
                message = f"{latlon}\nAddress: {address}"
        else:
            message = latlon
        self.append_text(message)

    def _resolve_address(self, latitude: float, longitude: float) -> str:
        try:
            response = requests.get(
                _GEOCODING_API,
                {
                    "latlng": f"{latitude},{longitude}",
                    "key": self._geolocation_api_key,
                }
            )
            response.raise_for_status()
            results = response.json().get('results')
            if results:
                return results[0]['formatted_address']
        except requests.RequestException:
            logger.exception("Failed to resolve address.")
        return ""

    def _write_record(self, record: str) -> None:
        with open(self._diary_file_path, "at") as fobj:
            fobj.write(record)


def naive_format(time: datetime.datetime, text: str) -> str:
    return _RECORD_PTRN.format(
        time=time.strftime(_TIME_FORMAT),
        text=text.strip(),
    )
