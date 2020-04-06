from unittest import TestCase

from diarybot.core.recorder import TextRecorder


class GetRecorderTestCase(TestCase):

    def setUp(self):
        self._recorder = TextRecorder(
            before_write=[self._on_before_write],
            on_write=[self._on_write],
            after_write=[self._on_after_write],
        )
        self.calls = []

    def test_append_sample_text(self):
        self._recorder.append_text('text')
        assert self.calls == [
            ('before_write',),
            ('on_write', 'text'),
            ('after_write',),
        ]

    def _on_before_write(self):
        self.calls.append(('before_write',))

    def _on_after_write(self):
        self.calls.append(('after_write',))

    def _on_write(self, text):
        self.calls.append(('on_write', text))
