from io import BytesIO
from typing import Dict, Iterable, List

from telegram import Update, Message, PhotoSize
from telegram.ext import (
    MessageHandler,
    Updater,
    Filters,
    CallbackContext,
)

from .tenant import Tenant, TenantNotFound
from .events import TextReceived, LocationReceived, VoiceReceived, EventReceived, PhotoReceived
from .handlers.loader import load_specs, EventSpec

_INSTALLATION_INSTRUCTIONS = """\
Hi, I'm GitDiaryBot (https://gitdiarybot.github.io/).
If you want to install it, send me a git repository URL
using following command template:

    /start git@github.com:peterdemin/diary.git

Note that you need to configure the repository to accept
my SSH public key:

"""

_INSTALLATION_SUCCEEDED = """\
Congrutalations, you I cloned your repository and ready to serve.
Try me, send me a test message and see how it gets to your diary.
"""


class TelegramReceiver:
    _LEGACY_FILTERS = [
        Filters.location,
        Filters.voice,
        Filters.photo,
    ]

    def __init__(self):
        self._tenants: Dict[int, Tenant] = {}
        self._event_specs: List[EventSpec] = load_specs()
        spec_filters = [
            event_spec.event_filter
            for event_spec in self._event_specs
        ]
        self._filters = tuple(spec_filters + self._LEGACY_FILTERS)

    def attach(self, bot: Updater) -> None:
        for filters in self._filters:
            bot.dispatcher.add_handler(MessageHandler(
                filters=filters,
                callback=self._on_event,
            ))

    def _on_event(self, update: Update, context: CallbackContext) -> None:
        del context  # Only need information from update
        if not update.message:
            return
        user_id = update.effective_user.id
        try:
            tenant = self._load_tenant(user_id)
        except TenantNotFound:
            self._attempt_install(user_id, update.message)
        else:
            for event in self._extract_events(update.message):
                tenant.handle_event(event)
            update.message.reply_text("Saved")

    @classmethod
    def _extract_events(cls, message: Message) -> Iterable[EventReceived]:
        for event_spec in self._event_specs:
            for event in event_spec.extractor(message):
                event_spec.handler(tenant).handle_event(event)
        if message.location:
            yield LocationReceived(
                message.location.latitude, message.location.longitude
            )
        if message.voice:
            fobj = BytesIO()
            tg_file = message.voice.get_file()
            tg_file.download(out=fobj)
            yield VoiceReceived(tg_file.file_id, fobj.getvalue())
        if message.photo:
            photo = cls._largest_photo(message.photo)
            tg_file = photo.get_file()
            fobj = BytesIO()
            tg_file.download(out=fobj)
            yield PhotoReceived(tg_file.file_id, fobj.getvalue())

    @staticmethod
    def _largest_photo(photo_sizes: List[PhotoSize]) -> PhotoSize:
        return max([
            (size.width * size.height, size)
            for size in photo_sizes
        ])[1]

    @staticmethod
    def _attempt_install(user_id: int, message: Message) -> None:
        if not message.text:
            message.reply_text(_INSTALLATION_INSTRUCTIONS)
            return
        if not message.text.startswith('/start'):
            message.reply_text(_INSTALLATION_INSTRUCTIONS)
        repo_url = message.text[7:]
        if not repo_url:
            message.reply_text(_INSTALLATION_INSTRUCTIONS)
        Tenant.install_repo_url(diary_dir=str(user_id), repo_url=repo_url)
        message.reply_text(_INSTALLATION_SUCCEEDED)

    def _load_tenant(self, user_id: int) -> Tenant:
        if user_id not in self._tenants:
            self._tenants[user_id] = Tenant.load(user_id)
        return self._tenants[user_id]
