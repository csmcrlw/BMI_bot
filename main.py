import os
from time import sleep
import telebot
from telebot import types

TOKEN = os.getenv('TELE_TOKEN')
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start_message(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton('Ок, давай начнём!'))
    bot.send_message(message.chat.id, 'Привет! Прежде чем мы начнём, хочу предупредить: информацию, предоставленную ботом, нельзя использовать /'
                                      'для постановки диагноза и в лечебных целях!', reply_markup=keyboard)

@bot.message_handler(content_types=["text"])
def know_weight(message):
    msg = bot.send_message(message.chat.id, 'Введи через запятую свои вес (в кг) и рост (в метрах). \nПример: 50, 1.65')
    bot.register_next_step_handler(msg, calc_bmi)

def calc_bmi(message):
    params = message.text.split(', ')
    w = float(params[0])
    h = float(params[1])
    i = round(w / (h**2), 1)

    bot.send_message(message.chat.id, f'Твой ИМТ: {i}')
    sleep(1)

    if i < 16:
        bot.send_message(message.chat.id, 'Выраженный дефицит массы тела. Необходимо обратиться к врачу!')
    elif 16 <= i < 18.5:
        bot.send_message(message.chat.id, 'Небольшой дефицит массы тела')
    elif 18.5 <= i < 25:
        bot.send_message(message.chat.id, 'Норма!')
    elif 25 <= i < 30:
        bot.send_message(message.chat.id, 'Масса тела немного выше нормы')
    elif 30 <= i < 35:
        bot.send_message(message.chat.id, 'Возможно ожирение 1 степени. Необходимо обратиться к врачу!')
    elif 35 <= i < 40:
        bot.send_message(message.chat.id, 'Возможно ожирение 2 степени. Необходимо обратиться к врачу!')
    elif i <= 40:
        bot.send_message(message.chat.id, 'Возможно ожирение 3 степени. Необходимо обратиться к врачу!')

#     msg = bot.send_message(message.chat.id, 'Хочешь получить рекомендации по питанию в соответствии с твоим ИМТ?)')
#     bot.register_next_step_handler(msg, give_recommendations)
#
# def give_recommendations(message):
#     pass

bot.polling(none_stop=True, interval=0)