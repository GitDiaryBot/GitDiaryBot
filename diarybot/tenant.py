import os
import attr

from .recorder import GitRecorder, GitSync
from .buy_list import BuyList
from .speech_to_text import SpeechToTextClient


_SINGLE_USER_ID = int(os.environ['SINGLE_USER_ID'])  # TODO: add multi-tenant mode


def load_tenant(user_id: int) -> 'Tenant':
    """Create Tenant library for Telegram user id."""
    if user_id != _SINGLE_USER_ID:
        raise ValueError(
            f"Rejected User ID {user_id} - doesn't match configured {_SINGLE_USER_ID}"
        )
    return Tenant(recorder=load_git_recorder())


def load_git_recorder() -> GitRecorder:
    base_dir = os.environ['DIARY_DIR']
    google_api_key = os.environ.get('DIARY_GOOGLE_API_KEY')
    recorder = GitRecorder(
        git_dir=base_dir,
        diary_file_name=os.environ.get('DIARY_FILE', 'README.md'),
        google_api_key=google_api_key,
        extra_text_handlers=[
            BuyList(os.path.join(base_dir, 'buy_list.md'))
        ],
        speech_to_text=SpeechToTextClient(google_api_key=google_api_key),
    )
    sync = GitSync(git_dir=base_dir)
    recorder.before_write.append(sync.on_before_write)
    recorder.after_write.append(sync.on_after_write)
    return recorder


@attr.s(slots=True, frozen=True, auto_attribs=True)
class Tenant:
    """Tenant-specific collection of objects."""
    recorder: GitRecorder
