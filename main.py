import telebot
from telebot import types
import webbrowser
import sqlite3

bot = telebot.TeleBot('')

name = None

@bot.message_handler(commands=['site'])
def site(message):
    webbrowser.open('https://itproger.com/course/telegram-bot')


# @bot.message_handler(commands=['start'])
# def main(message):
#     bot.send_message(message.chat.id, f'Hello, {message.from_user.first_name} {message.from_user.last_name}')

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('Перейти на сайт')
    markup.row(btn1)
    btn2 = types.KeyboardButton('Удалить фото')
    btn3 = types.KeyboardButton('Изменить текст')
    markup.row(btn2,btn3)
    # bot.reply_to(message,'Какое красивое фото', reply_markup = markup)
    file = open('./test.jpg','rb')
    #send_audio, send_video
    bot.send_photo(message.chat.id, file, reply_markup=markup)
    # bot.send_message(message.chat.id, f'Hello, {message.from_user.first_name} {message.from_user.last_name}', reply_markup=markup)
    bot.register_next_step_handler(message, on_click)

@bot.message_handler(commands=['database_start'])
def database_start(message):
    connection = sqlite3.connect('test1.sql')
    cursor = connection.cursor()

    cursor.execute('CREATE TABLE IF NOT EXISTS users(id int auto_increment primary key, name varchar(50), pass varchar(50))')
    connection.commit()
    cursor.close()
    connection.close()

    bot.send_message(message.chat.id, 'Привет, сейчас тебя зарегистрирую! Введите ваше имя')
    bot.register_next_step_handler(message, user_name)

def user_name(message):
    global name
    name = message.text.strip()
    bot.send_message(message.chat.id, 'Введите пароль')
    bot.register_next_step_handler(message, user_pass)

def user_pass(message):
    password = message.text.strip()

    connection = sqlite3.connect('test1.sql')
    cursor = connection.cursor()

    cursor.execute("INSERT INTO users(name, pass) VALUES ('%s','%s')" % (name, password))
    connection.commit()
    cursor.close()
    connection.close()


    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Список пользователей', callback_data='users'))
    bot.send_message(message.chat.id, 'Пользователь зарегестрирован', reply_markup=markup)
    #bot.register_next_step_handler(message, user_pass)

@bot.callback_query_handler(func = lambda callback: True)
def users(callback):
    connection = sqlite3.connect('test1.sql')
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    info = ''
    for el in users:
        info += f'Имя: {el[1]}, пароль: {el[2]}\n'
    cursor.close()
    connection.close()

    bot.send_message(callback.message.chat.id, info)

def on_click(message):
    if message.text == 'Перейти на сайт':
        bot.send_message(message.chat.id, 'Website is opened!')
    elif message.text == 'Удалить фото':
        bot.send_message(message.chat.id, 'Фото удалено!')
    elif message.text == 'Изменить текст':
        bot.send_message(message.chat.id, 'Текст изменен!')

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, '<b>Help</b> <em><u>information!</u></em>', parse_mode='html')

@bot.message_handler(content_types=['photo'])
def get_photo(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Перейти на сайт', url = 'https://itproger.com/course/telegram-bot')
    markup.row(btn1)
    btn2 = types.InlineKeyboardButton('Удалить фото', callback_data='delete')
    btn3 = types.InlineKeyboardButton('Изменить текст', callback_data='edit')
    markup.row(btn2,btn3)
    bot.reply_to(message,'Какое красивое фото', reply_markup = markup)


@bot.callback_query_handler(func = lambda callback: True)
def callback_message(callback):
    if callback.data == 'delete':
        bot.delete_message(callback.message.chat.id, callback.message.message_id-1)
    elif callback.data == 'edit':
        bot.edit_message_text('Edit Text', callback.message.chat.id, callback.message.message_id)

@bot.message_handler()
def info(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, f'Hello, {message.from_user.first_name} {message.from_user.last_name}')
    elif message.text.lower() == 'id':
        bot.reply_to(message, f'ID: {message.from_user.id}')


bot.infinity_polling()
