import telebot
import webbrowser

bot = telebot.TeleBot('7398190297:AAFCaJBm8fD6zdZir1Wggr-1xwb7s0cK_ao')


@bot.message_handler(commands=['site'])
def site(message):
    webbrowser.open('https://itproger.com/course/telegram-bot')


@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(message.chat.id, f'Hello, {message.from_user.first_name} {message.from_user.last_name}')


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, '<b>Help</b> <em><u>information!</u></em>', parse_mode='html')


@bot.message_handler()
def info(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, f'Hello, {message.from_user.first_name} {message.from_user.last_name}')
    elif message.text.lower() == 'id':
        bot.reply_to(message, f'ID: {message.from_user.id}')


bot.infinity_polling()
