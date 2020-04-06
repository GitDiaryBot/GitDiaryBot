#!/usr/bin/env python3

import os

from telegram.ext import Updater

from diarybot.dispatcher import TelegramDispatcher
from diarybot.extractors.extractor import EventExtractor
from diarybot.receiver import MessageReceiver, load_tenant_lib
from diarybot.skills import SKILLS


SINGLE_USER_ID = int(os.environ.get('SINGLE_USER_ID', '0'))
DIARY_TOKEN = os.environ['DIARY_TOKEN']


def run_forever():
    bot = Updater(DIARY_TOKEN, use_context=True)
    receiver = MessageReceiver(
        tenant_lib=load_tenant_lib(single_user_id=SINGLE_USER_ID),
        event_extractor=EventExtractor(skills=SKILLS),
    )
    dispatcher = TelegramDispatcher(message_receiver=receiver, skills=SKILLS)
    dispatcher.attach(bot)
    bot.start_polling()
    bot.idle()
