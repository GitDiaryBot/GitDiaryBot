import os
import configparser

import attr


_DEFAULT_DIARY_NAME = 'README.md'
_CONFIG_FILE_NAME = 'diary.ini'


@attr.s(slots=True, frozen=True, auto_attribs=True)
class TenantConfig:
    base_dir: str
    diary_file_name: str = _DEFAULT_DIARY_NAME
    google_api_key: str = None

    @classmethod
    def from_env(cls) -> 'TenantConfig':
        return cls(
            base_dir=os.environ['DIARY_DIR'],
            google_api_key=os.environ.get('DIARY_GOOGLE_API_KEY'),
            diary_file_name=os.environ.get('DIARY_FILE', _DEFAULT_DIARY_NAME),
        )

    @classmethod
    def from_user_directory(cls, directory_path: str) -> 'TenantConfig':
        if not os.path.isdir(directory_path):
            raise TenantNotFound(f"Tenant directory is missing at {directory_path}")
        config_path = os.path.join(directory_path, _CONFIG_FILE_NAME)
        google_api_key = None
        diary_file_name = _DEFAULT_DIARY_NAME
        if os.path.exists(config_path):
            config = configparser.ConfigParser()
            config.read(config_path)
            section = config['diary']
            google_api_key = section.get('diary_google_api_key', None)
            diary_file_name = section.get('diary_file', _DEFAULT_DIARY_NAME)
        return cls(
            base_dir=directory_path,
            google_api_key=google_api_key,
            diary_file_name=diary_file_name,
        )


class TenantConfigLoader:
    def __init__(self, single_user_id: int) -> None:
        self._single_user_id = single_user_id

    def load(self, user_id: int) -> TenantConfig:
        """Create Tenant library for Telegram user id."""
        if self._single_user_id:
            if user_id == self._single_user_id:
                return TenantConfig.from_env()
            raise NotSingleUser()
        return TenantConfig.from_user_directory(str(user_id))


class NotSingleUser(ValueError):
    """Bot runs in single user mode and tenant ID doesn't match it."""


class TenantNotFound(ValueError):
    """Attempted to load tenant that doesn't have a directory."""
