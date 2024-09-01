import telebot
import requests
import json
from config import BOT_TOKEN
from config import API

weather_bot = telebot.TeleBot(BOT_TOKEN)



@weather_bot.message_handler(commands=['start'])
def start_weather(message):
    weather_bot.send_message(message.chat.id, "Привет, рад тебя видеть! Напиши название города, пожалуйста:")

@weather_bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
    if res.status_code == 200:
        data = json.loads(res.text)
        temp = data["main"]["temp"]
        weather_bot.reply_to(message, f'{temp}')

        image = 'png-transparent-sun-logo-sunlight-silhouette-thumbnail.png' if temp > 5.0 else 'pngtree-cloud-and-sun-type-of-weather-png-image_6105935.png'
        file = open('./'+image, 'rb')
        weather_bot.send_photo(message.chat.id, file)
    else:
        weather_bot.reply_to(message, 'Город указан неверно')

weather_bot.infinity_polling()