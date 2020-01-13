import os
import attr

from .recorder import GitRecorder


_SINGLE_USER_ID = int(os.environ['SINGLE_USER_ID'])  # TODO: add multi-tenant mode


def load_tenant(user_id: int) -> 'Tenant':
    """Create Tenant library for Telegram user id."""
    if user_id != _SINGLE_USER_ID:
        raise ValueError(
            f"Rejected User ID {user_id} - doesn't match configured {_SINGLE_USER_ID}"
        )
    return Tenant(recorder=GitRecorder(
        git_dir=os.environ['DIARY_DIR'],
        diary_file_name=os.environ.get('DIARY_FILE', 'README.md'),
        geolocation_api_key=os.environ.get('GEOLOCATION_API_KEY')
    ))


@attr.s(slots=True, frozen=True, auto_attribs=True)
class Tenant:
    """Tenant-specific collection of objects."""
    recorder: GitRecorder
