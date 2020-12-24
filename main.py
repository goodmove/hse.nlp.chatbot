import os

import telebot
from dotenv import load_dotenv
from src.runtime import Runtime
from src.intent.classifier import IntentClassifier

load_dotenv()

API_TOKEN = os.getenv('API_TOKEN')

bot = telebot.TeleBot(API_TOKEN)
runtime = Runtime(IntentClassifier('data/models/knn'))

print('Runtime is set up')

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    response = None
    try:
        response = runtime.run(message.from_user.id, message.text)
    except Exception as e:
        response = 'Упс, что-то пошло не так'
        print(e)

    bot.send_message(message.from_user.id, response)


print('Bot polling is set up')
bot.polling(none_stop=True, interval=1)