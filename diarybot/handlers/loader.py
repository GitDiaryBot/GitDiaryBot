import os
from typing import Dict, Type

from diarybot.core.git_sync import GitSync
from diarybot.core.journal import PlainTextJournal
from diarybot.core.buy_list import BuyList
from diarybot.core.recorder import TextRecorder
from diarybot.core.speech_to_text import SpeechToTextClient
from diarybot.transformers.photo import PhotoTransformer
from diarybot.transformers.voice import VoiceTransformer
from diarybot.transformers.location import LocationTransformer
from diarybot.handlers.interface import EventHandler
from diarybot.tenant_config import TenantConfig
from diarybot.events import TextReceived, LocationReceived, VoiceReceived, PhotoReceived
from .text import TextEventHandler
from .location import LocationEventHandler
from .voice import VoiceEventHandler
from .photo import PhotoEventHandler


class HandlerLoader:
    def __init__(self, tenant_config: TenantConfig, recorder: TextRecorder) -> None:
        self._tenant_config = tenant_config
        self._recorder = recorder

    def load(self) -> Dict[Type, EventHandler]:
        return {
            TextReceived: self._load_text_event_handler(),
            LocationReceived: self._load_location_event_handler(),
            VoiceReceived: self._load_voice_event_handler(),
            PhotoReceived: self._load_photo_event_handler(),
        }

    def _load_text_event_handler(self) -> TextEventHandler:
        TextEventHandler(recorder=self._recorder)

    def _load_location_event_handler(self) -> LocationEventHandler:
        location_transformer = (
            LocationTransformer(self._tenant_config.google_api_key)
            if self._tenant_config.google_api_key
            else None
        )
        return LocationEventHandler(
            recorder=self._recorder,
            location_transformer=location_transformer,
        )

    def _load_voice_event_handler(self) -> VoiceEventHandler:
        speech_to_text = (
            SpeechToTextClient(google_api_key=self._tenant_config.google_api_key)
            if self._tenant_config.google_api_key
            else None
        )
        return VoiceEventHandler(
            recorder=self._recorder,
            voice_transformer=VoiceTransformer(
                base_dir=self._tenant_config.base_dir,
                speech_to_text=speech_to_text,
            ),
        )

    def _load_photo_event_handler(self) -> PhotoEventHandler:
        return PhotoEventHandler(
            recorder=self._recorder,
            photo_transformer=PhotoTransformer(
                base_dir=self._tenant_config.base_dir,
            ),
        )


def load_recorder(config: TenantConfig) -> TextRecorder:
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
