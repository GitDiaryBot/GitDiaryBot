from typing import List

from telegram import Update
from telegram.ext import (
    MessageHandler,
    Updater,
    CallbackContext,
)

from diarybot.receiver import MessageReceiver
from diarybot.tenant_config import TenantNotFound, NotSingleUser
from diarybot.skill_interface import Skill
from diarybot.guest import GuestReceiver


class TelegramDispatcher:
    """Dispatches incoming messages to message receiver or installer."""

    def __init__(self,
                 message_receiver: MessageReceiver,
                 guest_receiver: GuestReceiver,
                 skills: List[Skill]):
        self._message_receiver = message_receiver
        self._guest_receiver = guest_receiver
        self._filters = list({skill.tg_filter for skill in skills})

    def attach(self, bot: Updater) -> None:
        for filters in self._filters:
            bot.dispatcher.add_handler(MessageHandler(
                filters=filters,
                callback=self._on_update,
            ))

    def _on_update(self, update: Update, context: CallbackContext) -> None:
        del context  # Only need information from update
        if not update.message:
            return
        user_id = update.effective_user.id
        try:
            self._message_receiver.receive_message(user_id, update.message)
        except TenantNotFound:
            self._guest_receiver.handle_message(user_id, update.message)
        except NotSingleUser:
            update.message.reply_text(
                f"I'm running in single user mode and your user ID ({user_id}) doesn't match it."
            )
