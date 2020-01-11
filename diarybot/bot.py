#!/usr/bin/env python3

import os

from telegram.ext import Updater

from .receiver import TelegramReceiver


DIARY_TOKEN = os.environ['DIARY_TOKEN']


def run_forever():
    bot = Updater(DIARY_TOKEN, use_context=True)
    receiver = TelegramReceiver()
    receiver.attach(bot)
    bot.start_polling()
    bot.idle()
