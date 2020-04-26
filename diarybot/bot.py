#!/usr/bin/env python3

import os

from telegram.ext import Updater

from diarybot.dispatcher import TelegramDispatcher
from diarybot.extractors.extractor import EventExtractor
from diarybot.receiver import MessageReceiver, load_tenant_lib
from diarybot.skills import SKILLS
from diarybot.installer import TenantInstaller
from diarybot.guest import GuestReceiver


SINGLE_USER_ID = int(os.environ.get('SINGLE_USER_ID', '0'))
DIARY_TOKEN = os.environ.get('DIARY_TOKEN')


def run_forever():
    if not DIARY_TOKEN:
        raise RuntimeError("Environment variable DIARY_TOKEN is not set.")
    bot = Updater(DIARY_TOKEN, use_context=True)
    receiver = MessageReceiver(
        tenant_lib=load_tenant_lib(single_user_id=SINGLE_USER_ID, skills=SKILLS),
        event_extractor=EventExtractor(skills=SKILLS),
    )
    dispatcher = TelegramDispatcher(
        message_receiver=receiver,
        guest_receiver=GuestReceiver(TenantInstaller()),
        skills=SKILLS,
    )
    dispatcher.attach(bot)
    bot.start_polling()
    bot.idle()
