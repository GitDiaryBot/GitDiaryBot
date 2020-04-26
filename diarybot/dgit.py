import git


class Git:
    def __init__(self, repo: git.Repo) -> None:
        self._repo = repo

    def push(self):
        try:
            self._repo.remotes[0].push()
        except git.GitCommandError as exc:
            raise GitError(exc.stderr.strip()) from exc

    @classmethod
    def clone(cls, url: str, to_path: str) -> 'Git':
        try:
            repo = git.Repo.clone_from(url=url, to_path=to_path)
        except git.GitCommandError as exc:
            raise GitError(exc.stderr.strip()) from exc
        return cls(repo)


class GitError(RuntimeError):
    def __init__(self, stderr: str) -> None:
        self.stderr = stderr
        super().__init__(stderr)
