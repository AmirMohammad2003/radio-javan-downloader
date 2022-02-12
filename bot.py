from telnetlib import DO
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters

from downloader import Downloader

updater = Updater(
    "5233147023:AAFC3rUw4boaWksO2QMH8KEJT3uxGg8915A", use_context=True
)


def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Please send me the page link to get the download link."
    )


def unknown(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Sorry '{}' is not a valid command".format(update.message.text)
    )


def unknown_text(update: Update, context: CallbackContext):
    dl = Downloader(update.message.text)
    download_link = dl.get_download_link()
    # download_link = "hello, world!"
    update.message.reply_text("Here is the download link:\n{}".format(
        download_link
    ))


updater.dispatcher.add_handler(CommandHandler("start", start))
updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown))
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))

updater.start_polling()
