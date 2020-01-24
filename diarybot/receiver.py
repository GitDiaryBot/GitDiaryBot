from io import BytesIO
from typing import Dict

from telegram import Update, Voice, Message
from telegram.ext import (
    MessageHandler,
    Updater,
    Filters,
    CallbackContext,
)

from .tenant import Tenant


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
        self._handle_message(
            tenant=self._get_tenant(update.effective_user.id),
            message=update.message,
        )

    def _handle_message(self, tenant: Tenant, message: Message) -> None:
        if message.location:
            tenant.on_location(
                message.location.latitude, message.location.longitude
            )
        if message.text:
            tenant.on_text(message.text)
        if message.voice:
            self._on_voice(tenant, message.voice)
        message.reply_text("Saved")

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
