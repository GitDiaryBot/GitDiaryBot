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

    def attach(self, bot: Updater):
        bot.dispatcher.add_handler(MessageHandler(
            filters=Filters.text,
            callback=self._text_handler,
        ))

    def _text_handler(self, update: Update, context: CallbackContext) -> None:
        del context  # Only need information from update
        tenant = self._get_tenant(update.effective_user.id)
        tenant.recorder.append_text(update.message.text)
        update.message.reply_text("Saved")

    def _get_tenant(self, user_id: int) -> Tenant:
        if user_id not in self._tenants:
            self._tenants[user_id] = load_tenant(user_id)
        return self._tenants[user_id]
