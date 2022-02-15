import os
import logging

from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters

from downloader import Downloader
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

TOKEN = os.environ.get('TOKEN')

updater = Updater(
    TOKEN, use_context=True
)


def start(update: Update, context: CallbackContext):
    logger.info("Started: {}".format(update.effective_user.username))
    update.message.reply_text(
        "Please send the page link to get the download link."
    )


def unknown(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Sorry '{}' is not a valid command".format(update.message.text)
    )


def get_download_link(update: Update, context: CallbackContext):
    logger.info(update.message.text + ":" + update.effective_user.username)
    try:
        dl = Downloader(update.message.text)
        download_link = dl.get_download_link()
        update.message.reply_text("Here is the download link:\n{}".format(
            download_link
        ))

    except:
        update.message.reply_text("Something went wrong. Please try again.")


updater.dispatcher.add_handler(CommandHandler("start", start))
updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown))
updater.dispatcher.add_handler(MessageHandler(Filters.text, get_download_link))

PORT = int(os.environ.get('PORT', 8443))
updater.start_webhook(
    listen="0.0.0.0",
    port=int(PORT),
    url_path=TOKEN,
    webhook_url="https://rjdl.herokuapp.com/" + TOKEN
)
