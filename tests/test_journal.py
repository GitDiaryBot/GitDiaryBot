import io
import datetime
from unittest import mock

import pytz

from diarybot.core.journal import PlainTextJournal, naive_format


@mock.patch('diarybot.core.journal.open', create=True)
def test_append_sample_text(mock_open):
    journal = PlainTextJournal(file_path='file_path', text_formatter=fake_format)
    mock_open.return_value = mock.MagicMock(spec=io.IOBase)
    journal.handle_text('text')
    file_handle = mock_open.return_value.__enter__.return_value
    file_handle.write.assert_called_with('text')


def test_naive_formatter():
    record = naive_format(
        time=datetime.datetime(2014, 4, 14, 1, 2, 3, tzinfo=pytz.timezone('America/Chicago')),
        text='text',
    )
    assert record == '\n2014/04/14 01:02:03 LMT -0551\n\ntext\n'


def fake_format(time: datetime.datetime, text: str) -> str:
    del time  # ignore time for testability
    return text
