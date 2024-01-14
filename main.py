import os
import time
from datetime import datetime

import telebot
from dotenv import load_dotenv

# from search_bs4 import Search
from search_api import SearchAPI

load_dotenv()

token = os.environ['token']
bot = telebot.TeleBot(token)
users_timestamp = {}  # в словаре хранится id пользователя и time.time()


@bot.message_handler(commands=['start'])
def start_command(message):
    time.sleep(1)
    start_message = (f'<b>Поиск на</b> Plati.ru'
                     f'\n\nВыводятся три элемента из запроса:'
                     f'\n\t- с минимальной ценой'
                     f'\n\t- c максимальным рейтингом продавца'
                     f'\n\t- с максимальным числом продаж'
                     f'\n\nВведите запрос в строку:')

    try:
        users_timestamp[message.from_user.id]
    except KeyError:
        users_timestamp[message.chat.id] = int(time.time())  # добавляем запись о пользователе

    bot.send_message(message.chat.id, start_message, parse_mode='HTML')


@bot.message_handler(content_types=['text'])
def query(message):
    try:
        old_timestamp = users_timestamp[message.from_user.id]
    except KeyError:
        users_timestamp[message.chat.id] = int(time.time())  # добавляем запись о пользователе, если не добавились при команде /start
        return bot.send_message(message.chat.id, 'Повторите запрос')
    else:
        if (int(time.time()) - old_timestamp) < 5:  # считаем время между запросами
            return bot.send_message(message.chat.id, 'Ошибка. Подождите 5 секунд между запросами')
        else:
            users_timestamp[message.chat.id] = int(time.time())

            if message.text.startswith('/'):
                bot.send_message(message.from_user.id, "Ошибка. Запрос не может начинаться с '/'")
            else:
                bot.send_message(message.from_user.id, 'Поиск...')
                result = SearchAPI(message.text).get_result()

                if not result:
                    bot.send_message(message.from_user.id, 'Ничего не найдено')
                else:
                    bot.send_message(message.from_user.id, f'Найдено всего: {result[-1]}')

                    for i in result[:-1]:
                        bot.send_message(message.from_user.id, i, parse_mode='HTML', disable_web_page_preview=True)


bot.infinity_polling()
