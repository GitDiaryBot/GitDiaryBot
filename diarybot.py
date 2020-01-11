import os
import logging

from telegram.ext import MessageHandler
from telegram.ext import Updater
from telegram.ext import Filters


TG_TOKEN = os.environ['DIARY_TOKEN']
TG_API_URL = "https://telegg.ru/orig/bot"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)


def main():
    bot = Updater(TG_TOKEN, TG_API_URL, use_context=True)
    bot.dispatcher.add_handler(MessageHandler(Filters.text, parrot))
    bot.start_polling()  # проверяет о наличии сообщений с платформы Telegram
    bot.idle()  # бот будет работать пока его не остановят


def parrot(bot, update):
    print(bot.message.text)  # печатаем на экран сообщение пользователя
    bot.message.reply_text(bot.message.text)  # отправляем обратно текс который пользователь послал


if __name__ == '__main__':
    main()
