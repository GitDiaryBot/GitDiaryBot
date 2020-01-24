import os
import attr

from .recorder import TextRecorder
from .git_sync import GitSync
from .buy_list import BuyList
from .journal import PlainTextJournal, DEFAULT_DIARY_NAME
from .speech_to_text import SpeechToTextClient
from .transformers.location import LocationTransformer
from .transformers.voice import VoiceTransformer


_SINGLE_USER_ID = int(os.environ['SINGLE_USER_ID'])  # TODO: add multi-tenant mode


@attr.s(slots=True, frozen=True, auto_attribs=True)
class Tenant:
    """Tenant-specific collection of objects."""
    recorder: TextRecorder
    location_transformer: LocationTransformer
    voice_transformer: VoiceTransformer

    def on_text(self, text: str) -> None:
        self.recorder.append_text(text)

    def on_location(self, latitude: float, longitude: float) -> None:
        message = self.location_transformer.handle_coordinates(
            latitude, longitude
        )
        self.on_text(message)

    def on_voice(self, file_id: str, data: bytes) -> None:
        with self.voice_transformer.file_writer(file_id) as fobj:
            fobj.write(data)
        message = self.voice_transformer.handle_file_id(file_id)
        self.on_text(message)

    @classmethod
    def load(cls, user_id: int) -> 'Tenant':
        """Create Tenant library for Telegram user id."""
        if user_id != _SINGLE_USER_ID:
            raise ValueError(
                f"Rejected User ID {user_id} - doesn't match configured {_SINGLE_USER_ID}"
            )
        return cls.from_config(cls.load_env_config())

    @classmethod
    def from_config(cls, config: 'TenantConfig') -> 'Tenant':
        speech_to_text = (
            SpeechToTextClient(google_api_key=config.google_api_key)
            if config.google_api_key
            else None
        )
        return cls(
            recorder=cls._load_text_recorder(config),
            location_transformer=LocationTransformer(config.google_api_key),
            voice_transformer=VoiceTransformer(
                base_dir=config.base_dir,
                speech_to_text=speech_to_text,
            ),
        )

    @classmethod
    def load_env_config(cls) -> 'TenantConfig':
        return TenantConfig(
            base_dir=os.environ['DIARY_DIR'],
            google_api_key=os.environ.get('DIARY_GOOGLE_API_KEY'),
            diary_file_name=os.environ.get('DIARY_FILE', DEFAULT_DIARY_NAME),
        )

    @staticmethod
    def _load_text_recorder(config: 'TenantConfig') -> TextRecorder:
        sync = GitSync(git_dir=config.base_dir)
        journal_path = os.path.join(config.base_dir, config.diary_file_name)
        return TextRecorder(
            before_write=[sync.on_before_write],
            on_write=[
                PlainTextJournal(file_path=journal_path),
                BuyList(os.path.join(config.base_dir, 'buy_list.md')),
            ],
            after_write=[sync.on_after_write],
        )


@attr.s(slots=True, frozen=True, auto_attribs=True)
class TenantConfig:
    base_dir: str
    diary_file_name: str
    google_api_key: str = None
