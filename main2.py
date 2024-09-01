import telebot
from telebot import types
from telebot.types import WebAppInfo
from config import BOT_TOKEN

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup()
    markup.add(types.KeyboardButton("Открыть веб страницу", web_app=WebAppInfo(url='https://github.com/IvanShalimov/telegram-bot-tutorial-number-one/blob/master/index.html')))
    bot.send_message(message.chat.id,'Привет, мой друг!', reply_markup= markup)

bot.infinity_polling()