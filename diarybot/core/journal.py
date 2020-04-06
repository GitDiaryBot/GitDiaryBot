import datetime
from typing import Callable

import tzlocal

from .text_handler import TextHandler


DEFAULT_DIARY_NAME = 'README.md'
_RECORD_PTRN = """
{time}

{text}
"""
_TIME_FORMAT = '%Y/%m/%d %H:%M:%S %Z %z'


class PlainTextJournal(TextHandler):

    def __init__(self,
                 file_path: str,
                 text_formatter: Callable = None) -> None:
        self._file_path = file_path
        self._format = text_formatter or naive_format

    def handle_text(self, text: str) -> None:
        # TODO: make time zone configurable
        now = datetime.datetime.now(tzlocal.get_localzone())
        record = self._format(now, text)
        with open(self._file_path, "at") as fobj:
            fobj.write(record)


def naive_format(time: datetime.datetime, text: str) -> str:
    return _RECORD_PTRN.format(
        time=time.strftime(_TIME_FORMAT),
        text=text.strip(),
    )
