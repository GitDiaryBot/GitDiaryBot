from typing import List

from telegram import Update, Message
from telegram.ext import (
    MessageHandler,
    Updater,
    CallbackContext,
)

from diarybot.receiver import MessageReceiver
from diarybot.tenant_config import TenantNotFound
from diarybot.tenant import Tenant
from diarybot.skill_interface import Skill

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


class TelegramDispatcher:
    """Dispatches incoming messages to message receiver or installer."""

    def __init__(self, message_receiver: MessageReceiver, skills: List[Skill]):
        self._message_receiver = message_receiver
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
            self._attempt_install(user_id, update.message)

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
