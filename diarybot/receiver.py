from io import BytesIO
from typing import Dict

from telegram import Update, Voice, Message
from telegram.ext import (
    MessageHandler,
    Updater,
    Filters,
    CallbackContext,
)

from .tenant import Tenant, TenantNotFound

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

    FILTERS = (
        Filters.text,
        Filters.location,
        Filters.voice,
    )

    def __init__(self):
        self._tenants: Dict[int, Tenant] = {}

    def attach(self, bot: Updater):
        for filters in self.FILTERS:
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
            self.handle_message(
                tenant=self._get_tenant(user_id),
                message=update.message,
            )
        except TenantNotFound:
            self._attempt_install(user_id, update.message)
        else:
            update.message.reply_text("Saved")

    def handle_message(self, tenant: Tenant, message: Message) -> None:
        if message.location:
            tenant.on_location(
                message.location.latitude, message.location.longitude
            )
        if message.text:
            tenant.on_text(message.text)
        if message.voice:
            self._on_voice(tenant, message.voice)

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

    @staticmethod
    def _on_voice(tenant: Tenant, voice: Voice) -> None:
        fobj = BytesIO()
        tg_file = voice.get_file()
        tg_file.download(out=fobj)
        tenant.on_voice(tg_file.file_id, fobj.getvalue())

    def _get_tenant(self, user_id: int) -> Tenant:
        if user_id not in self._tenants:
            self._tenants[user_id] = Tenant.load(user_id)
        return self._tenants[user_id]
