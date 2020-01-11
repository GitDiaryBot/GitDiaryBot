#!/usr/bin/env python3

import os
import logging
import datetime

from telegram.ext import MessageHandler
from telegram.ext import Updater
from telegram.ext import Filters
import git
import tzlocal


DIARY_TOKEN = os.environ['DIARY_TOKEN']
DIARY_DIR = os.environ['DIARY_DIR']
DIARY_FILE = os.environ.get('DIARY_FILE', 'README.md')
DIARY_FILE_PATH = os.path.join(DIARY_DIR, DIARY_FILE)
RECORD_PTRN = """
{time}

{text}
"""


def main():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    bot = Updater(DIARY_TOKEN, use_context=True)
    bot.dispatcher.add_handler(MessageHandler(
        filters=Filters.text,
        callback=handler,
    ))
    bot.start_polling()
    bot.idle()


def handler(update, context):
    del context  # TODO: choose settings for user
    add_record(update.message.text)
    update.message.reply_text("Saved")


def add_record(text: str):
    now = datetime.datetime.now(tzlocal.get_localzone())
    repo = git.Repo(DIARY_DIR)
    repo.remotes[0].pull()
    write_record(now, text)
    repo.index.add(DIARY_FILE)
    repo.index.commit("add record from GitDiaryBot")
    repo.remotes[0].push()


def write_record(time: datetime.datetime, text: str):
    with open(DIARY_FILE_PATH, "at") as fp:
        fp.write(RECORD_PTRN.format(
            time=time.strftime('%Y/%m/%d %H:%M:%S %Z %z'),
            text=text,
        ))


if __name__ == '__main__':
    main()
