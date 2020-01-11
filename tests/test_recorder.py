import io
from unittest import mock, TestCase
import datetime

import git
import pytz

from diarybot.recorder import GitRecorder, naive_format


class GetRecorderTestCase(TestCase):

    def setUp(self):
        self._recorder = GitRecorder(
            git_dir='dir',
            diary_file_name='file',
            repo_class=lambda x: mock.MagicMock(spec=git.Repo),
            text_formatter=fake_format,
        )

    @mock.patch('diarybot.recorder.open', create=True)
    def test_append_sample_text(self, mock_open):
        mock_open.return_value = mock.MagicMock(spec=io.IOBase)
        self._recorder.append_text('text')
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
