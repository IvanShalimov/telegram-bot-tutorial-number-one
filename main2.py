import telebot
from telebot import types
from telebot.types import WebAppInfo

bot = telebot.TeleBot('')

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup()
    markup.add(types.KeyboardButton("Открыть веб страницу", web_app=WebAppInfo(url='https://itproger.com')))
    bot.send_message(message.chat.id,'Привет, мой друг!', reply_markup= markup)

bot.infinity_polling()