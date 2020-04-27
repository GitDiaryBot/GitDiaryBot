#!/usr/bin/env python3

import os

from telegram.ext import Updater

from diarybot.dispatcher import TelegramDispatcher
from diarybot.extractors.extractor import EventExtractor
from diarybot.receiver import MessageReceiver, load_tenant_lib
from diarybot.skills import SKILLS
from diarybot.installer import TenantInstaller
from diarybot.guest import GuestReceiver
from diarybot.bot_config import BOT_CONFIG
from diarybot.dgit import GitOps


DIARY_TOKEN = os.environ.get('DIARY_TOKEN')


def run_forever():
    if not BOT_CONFIG.telegram_token:
        raise RuntimeError("Environment variable DIARY_TOKEN is not set.")
    bot = Updater(BOT_CONFIG.telegram_token, use_context=True)
    receiver = MessageReceiver(
        tenant_lib=load_tenant_lib(
            bot_config=BOT_CONFIG,
            skills=SKILLS,
        ),
        event_extractor=EventExtractor(skills=SKILLS),
    )
    dispatcher = TelegramDispatcher(
        message_receiver=receiver,
        guest_receiver=GuestReceiver(
            TenantInstaller(
                gitops=GitOps(BOT_CONFIG.private_key_path)
            )
        ),
        skills=SKILLS,
    )
    dispatcher.attach(bot)
    bot.start_polling()
    bot.idle()
