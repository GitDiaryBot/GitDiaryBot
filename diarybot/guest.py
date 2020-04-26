from telegram import Message

from diarybot.installer import TenantInstaller


class GuestReceiver:
    def __init__(self, installer: TenantInstaller) -> None:
        self._installer = installer

    def handle_message(self, user_id: int, message: Message) -> None:
        message.reply_text(
            self._installer.respond(user_id, message.text)
        )
