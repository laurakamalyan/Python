import telebot
import requests
import json

bot = telebot.TeleBot('6650526253:AAGWDSmpeOmIKzu4o0JVYeY7jha-XPBimQA')
API = 'f6ecf21f5aed0dabc3a1488c46fbec29'


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Input city name")


@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip().lower()

    res = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric")
    if res.status_code == 200:
        data = json.loads(res.text)
        temp = data['main']['temp']
        temp_min = data['main']['temp_min']
        temp_max = data['main']['temp_max']
        cloud = data['clouds']['all']

        if 0 <= cloud < 20: image = 'sunny.jpg'
        elif 20 <= cloud < 60: image = 'sunny-cloudy.jpg'
        elif cloud >= 60: image = 'cloudy.jpg'

        file = open('./img/' + image, 'rb')
        bot.send_photo(message.chat.id, file)

        bot.send_message(message.chat.id, f"Weather now: {temp}")
        bot.send_message(message.chat.id, f"Min: {temp_min}°, max: {temp_max}°")


    else:
        bot.send_message(message.chat.id, "wrong city name")


bot.infinity_polling()