import telebot
from currency_converter import CurrencyConverter
from telebot import types

bot = telebot.TeleBot('')
currency = CurrencyConverter()
amount = 0

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет, введите сумму')
    bot.register_next_step_handler(message, summa)

def summa(message):
    global amount
    try:
        amount = int(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, 'Неверный формат, введите сумму')
        bot.register_next_step_handler(message, summa)
        return

    if amount > 0:
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton('USD/EUR', callback_data='usd/eur')
        btn2 = types.InlineKeyboardButton('EUR/USD', callback_data='eur/usd')
        btn3 = types.InlineKeyboardButton('USD/GBP', callback_data='usd/gpb')
        btn4 = types.InlineKeyboardButton('Другое значение', callback_data='else')
        markup.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.chat.id, 'Выберите пару валют', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Число должно быть больше 0, введите сумму')
        bot.register_next_step_handler(message, summa)
        return

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data != 'else':
        value = call.data.upper().split('/')
        res = currency.convert(amount,value[0],value[1])
        bot.send_message(call.message.chat.id, f'Получается {round(res, 2)}. Можете заново списать сумму')
        bot.register_next_step_handler(call.message, summa)
    else:
        bot.send_message(call.message.chat.id, 'Введите пару значений через слеш')
        bot.register_next_step_handler(call.message, mycurrency)

def mycurrency(message):
    try:
        value = message.data.upper().split('/')
        res = currency.convert(amount, value[0], value[1])
        bot.send_message(message.message.chat.id, f'Получается {round(res, 2)}. Можете заново списать сумму')
        bot.register_next_step_handler(message.message, summa)
    except Exception:
        bot.send_message(message.message.chat.id, f'Что-то не так, впишите значение заново:')
        bot.register_next_step_handler(message.message, summa)

bot.infinity_polling()