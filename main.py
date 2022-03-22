import site_parser

from telegram.ext import Updater
import logging
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from boto.s3.connection import S3Connection  # api token access

# webhook stuff
import os
PORT = int(os.environ.get('PORT', 5000))  # port to listen in for the webhook



def start(update: Update, context: CallbackContext):
    text = "Привет, я умею искать объявления по запросу на популярных площадках. Напиши запрос, и я поищу что-нибудь."
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


def help(update: Update, context: CallbackContext):
    text = "Какая-то инструкция"
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


def unknown_command(update: Update, context: CallbackContext):
    text = "Нет такой команды"
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


def query(update: Update, context: CallbackContext):
    search_query = update.message.text
    text = f"Сейчас что-нибудь поищу по запросу '{search_query}'..."
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)

    data = site_parser.search_by_query(sites=['avito'], query=search_query, city="nizhniy_novgorod", num_listings=5)
    for datum in data:
        listing_message_text = f"{datum['title']}\nЦена: {datum['price']}\n" \
                               f"Описание: {datum['description']}\nСсылка: {datum['link']}"
        context.bot.send_message(chat_id=update.effective_chat.id, text=listing_message_text)
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=datum['img_link'])


def main(TOKEN):
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    # /start handler #
    dispatcher.add_handler(CommandHandler('start', start))

    # /help handler #
    dispatcher.add_handler(CommandHandler('help', help))

    # invalid command handler #
    dispatcher.add_handler(MessageHandler(Filters.command, unknown_command))

    # text message handler #
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, query))

    # start the bot #
    # updater.start_polling()
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook('https://listing-telegram-bot.herokuapp.com/' + TOKEN)

    updater.idle()


if __name__ == "__main__":
    TOKEN = ''
    # with open("api_token.txt", 'r') as fin:
    #     TOKEN = fin.read()

    TOKEN = os.environ['API_TOKEN']
    # TODO: error when no file

    # site_parser.search_by_query(sites=['avito'], query="лего", city="nizhniy_novgorod", num_listings=5)

    main(TOKEN)
