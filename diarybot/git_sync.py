from typing import Callable

import git


_COMMIT_MESSAGE = 'add record from GitDiaryBot'


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
