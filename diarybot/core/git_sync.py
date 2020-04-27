from diarybot.dgit import Git


_COMMIT_MESSAGE = 'add record from GitDiaryBot'


class GitSync:
    """Directory synchronization using Git repository."""

    def __init__(self, git: Git) -> None:
        self._git = git

    def on_before_write(self) -> None:
        """Download remote changes."""
        self._git.maybe_pull()

    def on_after_write(self) -> None:
        """Upload local changes."""
        self._git.maybe_push(_COMMIT_MESSAGE)
