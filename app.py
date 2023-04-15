import traceback

import telebot

from config import *
from extensions import APIException, Converter


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands= ['start', 'help'])
def help(message: telebot.types.Message):
    text = "Привет, этот бот помогает конвентировать валюты." \
           " Чтобы получить нужную информацию введите сообщение в виде:" \
           "<имя вашей валюты><имя валюты, в которую надо конвертировать>" \
           "<количество вашей валюты>" \
           "Чтобы посмотреть список доступных валют вызовите /values "
    bot.reply_to(message, text)

@bot.message_handler(commands= ['values'])
def values(message: telebot.types.Message):
    text = "Доступные валюты:"
    for key in exchanges.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    values = message.text.split()
    try:
        if len(values) != 3:
            raise APIException("Неверное количество параметров.")

        answer = Converter.get_price(*values)
    except APIException as e:
        bot.reply_to(message, f"Ошибка в команде: \n{e}")
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        bot.reply_to(message, f"Неизвестная ошибка: \n{e}")
    else:
        bot.send_message(message.chat.id, answer)


bot.polling()
