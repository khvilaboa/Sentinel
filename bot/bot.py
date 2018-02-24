
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler

updater = Updater(token='470195902:AAEsYMKz9jwypqfEMw8nOPAxF6QhyzQuETY')  # @TrafficSentinelBot
dispatcher = updater.dispatcher

COORDS_URL = "localhost:8000/app/map?long={long}&lang={lat}"

def start(bot, update):
	update.message.reply_text("Starting...")

	
def location(bot, update):
	loc = update.message.location
	url = COORDS_URL.format(long = loc.longitude, lat = loc.latitude)
	update.message.reply_text(url)

# Handlers
dispatcher.add_handler(CommandHandler('start', start))
#dispatcher.add_handler(MessageHandler(Filters.text, text))
#dispatcher.add_handler(MessageHandler(Filters.command, unknown))
#dispatcher.add_handler(MessageHandler(Filters.photo, images))
dispatcher.add_handler(MessageHandler(Filters.location, location))
#updater.dispatcher.add_handler(CallbackQueryHandler(keyboard_press))  # To handle keyboard press

updater.start_polling()  # Starts the bot
