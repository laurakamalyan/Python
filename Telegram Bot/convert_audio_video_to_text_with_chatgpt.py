import telebot
import openai
from urllib.request import urlretrieve
from telebot import types

telegram_key = '6574685351:AAFRw0f2ydeID3cJ5yqTANGWfnp12PKsqSg'
gpt_key = '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'

bot = telebot.TeleBot(telegram_key)

file_url=None
file_name=None


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Hello. Send your audio or video file here and I will convert it to text.')


@bot.message_handler(content_types=['audio', 'video'])
def open_file(message):
    global file_name
    global file_url

    if message.audio:
        file_url = bot.get_file_url(message.audio.file_id)
        file_name = message.audio.file_name
    elif message.video:
        file_url = bot.get_file_url(message.video.file_id)
        file_name = message.video.file_name

    urlretrieve(file_url, f'{file_name}')
    file = open(f'./{file_name}', 'rb')

    result = openai.Audio.transcribe(
        api_key=gpt_key,
        model='whisper-1',
        file=file,
        response_format='text'
    )

    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton('Translate to english', callback_data='translate to english')
    markup.row(btn)

    bot.reply_to(message, result, reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    global file_name
    global file_url

    if callback.message.audio:
        file_url = bot.get_file_url(callback.message.audio.file_id)
        file_name = callback.message.audio.file_name
    elif callback.message.video:
        file_url = bot.get_file_url(callback.message.video.file_id)
        file_name = callback.message.video.file_name

    urlretrieve(file_url, f'{file_name}')
    file = open(f'./{file_name}', 'rb')

    result = openai.Audio.translate(
        api_key=gpt_key,
        model='whisper-1',
        file=file,
        response_format='text'
    )

    bot.reply_to(callback.message, result)


bot.infinity_polling()
