from typing import Callable

import git


_COMMIT_MESSAGE = 'add record from GitDiaryBot'


class GitSync:
    """Directory synchronization using Git repository."""

    def __init__(self, git_dir: str, repo_class: Callable = git.Repo) -> None:
        self._repo = repo_class(git_dir)

    def on_before_write(self) -> None:
        """Download remote changes."""
        if self._is_clean():
            self._repo.remotes[0].pull()

    def on_after_write(self) -> None:
        """Upload local changes."""
        self._repo.git.add(A=True)
        if not self._is_clean():
            self._repo.index.commit(_COMMIT_MESSAGE)
            self._repo.remotes[0].push()

    def _is_clean(self) -> bool:
        return not self._repo.is_dirty()
