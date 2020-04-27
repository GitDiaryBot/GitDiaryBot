import os

import attr


@attr.s(slots=True, frozen=True, auto_attribs=True)
class BotConfig:
    single_user_id: int
    telegram_token: str
    private_key_path: str


def load_bot_config_from_env() -> BotConfig:
    return BotConfig(
        single_user_id=int(os.environ.get('SINGLE_USER_ID', '0')),
        telegram_token=os.environ.get('DIARY_TOKEN', ''),
        private_key_path=os.environ.get('DIARY_ID_RSA', ''),
    )


BOT_CONFIG = load_bot_config_from_env()
