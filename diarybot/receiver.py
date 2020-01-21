from typing import Dict

from telegram import Update
from telegram.ext import (
    MessageHandler,
    Updater,
    Filters,
    CallbackContext,
)

from .tenant import Tenant


class TelegramReceiver:

    def __init__(self):
        self._tenants: Dict[int, Tenant] = {}
        self._handlers = (
            (Filters.text, self._on_text),
            (Filters.location, self._on_location),
            (Filters.voice, self._on_voice),
        )

    def attach(self, bot: Updater):
        for filters, callback in self._handlers:
            bot.dispatcher.add_handler(MessageHandler(
                filters=filters,
                callback=callback,
            ))

    def _on_text(self, update: Update, context: CallbackContext) -> None:
        del context  # Only need information from update
        tenant = self._get_tenant(update.effective_user.id)
        tenant.recorder.append_text(update.message.text)
        update.message.reply_text("Saved")

    def _on_location(self, update: Update, context: CallbackContext) -> None:
        del context  # Only need information from update
        tenant = self._get_tenant(update.effective_user.id)
        message = tenant.location_transformer.handle_coordinates(
            latitude=update.message.location.latitude,
            longitude=update.message.location.longitude,
        )
        tenant.recorder.append_text(message)
        update.message.reply_text("Saved")

    def _on_voice(self, update: Update, context: CallbackContext) -> None:
        del context  # Only need information from update
        tenant = self._get_tenant(update.effective_user.id)
        tg_file = update.message.voice.get_file()
        with tenant.voice_transformer.file_writer(tg_file.file_id) as fobj:
            tg_file.download(out=fobj)
        message = tenant.voice_transformer.handle_file_id(tg_file.file_id)
        tenant.recorder.append_text(message)
        update.message.reply_text("Saved")

    def _get_tenant(self, user_id: int) -> Tenant:
        if user_id not in self._tenants:
            self._tenants[user_id] = Tenant.load(user_id)
        return self._tenants[user_id]
