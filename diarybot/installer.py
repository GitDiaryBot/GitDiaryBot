from diarybot.dgit import Git, GitError


_INSTALLATION_INSTRUCTIONS = """\
Hi, I'm GitDiaryBot (https://gitdiarybot.github.io/).
If you want to install it, send me a git repository URL
using following command template:

    /start git@github.com:peterdemin/diary.git

Note that you need to configure the repository to give me write access.
"""

_INSTALLATION_SUCCEEDED = """\
Congrutalations, I cloned your repository and ready to serve.
Send me a message and see how it gets into your diary.
"""

_CLONE_FAILED = """\
Failed to clone the repository. Here's the error from git:
"""

_FOLLOW_INSTRUCTIONS = """\
Please follow installation instruction at https://gitdiarybot.github.io/#install
"""

_NO_WRITE_ACCESS = """\
I cloned the repository, but it looks like I don't have the permissions to push changes.
Here's the error from git:
"""

_CHEER_UP = """\
Once it's done, no additional setup required, you can start journaling.
"""


class TenantInstaller:
    _TRIGGER = '/start'

    def respond(self, user_id: int, message: str = None) -> str:
        """Generate response text for unknown user.

        1. Clone the repo provided in the /start command.
        2. Verify that ``git push`` succeeds.
        3. Return success message if all is good.
        4. Return error message if something is wrong.
        """
        if not self._is_valid_request(message):
            return _INSTALLATION_INSTRUCTIONS + _FOLLOW_INSTRUCTIONS
        repo_url = message[len(self._TRIGGER) + 1:].strip()
        try:
            repo = Git.clone(url=repo_url, to_path=str(user_id))
        except GitError as exc:
            return "{}\n{}\n{}".format(_CLONE_FAILED, exc.stderr, _FOLLOW_INSTRUCTIONS)
        try:
            repo.push()
        except GitError as exc:
            return "{}\n{}\n{}\n{}".format(
                _NO_WRITE_ACCESS, exc.stderr, _FOLLOW_INSTRUCTIONS, _CHEER_UP
            )
        return _INSTALLATION_SUCCEEDED

    def _is_valid_request(self, message: str = None) -> bool:
        if message and message.startswith(self._TRIGGER):
            repo_url = message[len(self._TRIGGER) + 1:].strip()
            if repo_url:
                return True
        return False


class InvalidInstallationRequest(ValueError):
    pass
