from unittest import TestCase, mock

from git.remote import Remote
from git.index import IndexFile

from diarybot.core.git_sync import GitSync


class GitSyncTestCase(TestCase):

    def setUp(self):
        self._fake_repo = FakeRepo()
        self._git_sync = GitSync(git_dir='git_dir', repo_class=self._fake_repo)

    def test_sets_git_dir(self):
        assert self._fake_repo.git_dir == 'git_dir'

    def test_pulls_before_write(self):
        self._git_sync.on_before_write()
        self._fake_repo.remotes[0].pull.assert_called_once_with()

    def test_skips_pull_in_dirty_index(self):
        self._fake_repo.dirty = True
        self._git_sync.on_before_write()
        self._fake_repo.remotes[0].pull.assert_not_called()

    def test_pushes_after_write(self):
        self._fake_repo.dirty = True
        self._git_sync.on_after_write()
        self._fake_repo.index.commit.assert_called_once_with(mock.ANY)
        self._fake_repo.remotes[0].push.assert_called_once_with()

    def test_skips_commit_if_nothing_changed(self):
        self._fake_repo.dirty = False
        self._git_sync.on_after_write()
        self._fake_repo.index.commit.assert_not_called()
        self._fake_repo.remotes[0].push.assert_not_called()


class FakeRepo:

    def __init__(self):
        self.git_dir = None
        self.git = mock.Mock()
        self.index = mock.Mock(spec=IndexFile)
        self.remotes = [mock.Mock(spec=Remote)]
        self.dirty = False

    def __call__(self, git_dir: str) -> 'FakeRepo':
        self.git_dir = git_dir
        return self

    def is_dirty(self):
        return self.dirty
