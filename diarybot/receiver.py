from typing import Dict

from telegram import Update
from telegram.ext import (
    MessageHandler,
    Updater,
    Filters,
    CallbackContext,
)

from .recorder import GitRecorder
from .tenant import load_tenant, Tenant


class TelegramReceiver:

    def __init__(self):
        self._tenants: Dict[int, GitRecorder] = {}
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
        tenant.recorder.append_location(
            update.message.location.latitude,
            update.message.location.longitude,
        )
        update.message.reply_text("Saved")

    def _on_voice(self, update: Update, context: CallbackContext) -> None:
        del context  # Only need information from update
        tenant = self._get_tenant(update.effective_user.id)
        tg_file = update.message.voice.get_file()
        with tenant.recorder.append_audio(tg_file.file_id) as fobj:
            tg_file.download(out=fobj)
        update.message.reply_text("Saved")

    def _get_tenant(self, user_id: int) -> Tenant:
        if user_id not in self._tenants:
            self._tenants[user_id] = load_tenant(user_id)
        return self._tenants[user_id]
