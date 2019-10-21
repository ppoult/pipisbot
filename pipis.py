import vk_api
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests
import os
import random
import re
import json, apiai
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO) #enable logging

def GetShit(): #сгребаем последнюю запись со стены Pipis

    login, password = 'flokinokinihilipilifications@mail.ru', 'WSK741qaz'
    vk_session = vk_api.VkApi(login, password)

    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    vk = vk_session.get_api()

    response = vk.wall.get(domain='pipis_everyday', count=1)  # Используем метод wall.get
    response_two = response['items'][0]['text'] #parsing the JSON output for the text block
    return response_two #return the variable with the text

def GetPic(): #сгребаем картинку со стены Pipis

    login, password = 'flokinokinihilipilifications@mail.ru', 'WSK741qaz' #authenticate
    vk_session = vk_api.VkApi(login, password)

    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    vk = vk_session.get_api()

    response = vk.wall.get(domain='pipis_everyday', count=1)  # Используем метод wall.get с VK.python
    response_three = response['items'][0]['attachments'][0]['photo']['sizes'][4]['url'] #parsing the JSON output for the text block
    return response_three #return the variable with the pic url



def start(update, context):  #greetings function
    context.bot.send_message(chat_id=update.effective_chat.id, text='Привет. Я — Пипис, полиморфный цыпленок. Могу подскзать, какой сегодня день.')

def ask(update, context): #picture of the day function. Get all the return variables and paste them into the reply
    answer = GetShit()
    pic = GetPic()
    context.bot.send_message(chat_id=update.effective_chat.id, text='Бакаа, бкааа...бкаа, бка')
    context.bot.send_message(chat_id=update.effective_chat.id, text=answer)
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=pic)

def roll(update, context):
    directory = "pics/"
    random_image = random.choice(os.listdir(directory))
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(directory + random_image,'rb'))

def textMessage(update, context):
    request = apiai.ApiAI('b746273a2e4c49f8b91d9fe91784d15a').text_request() # Токен API к Dialogflow
    request.lang = 'ru' # На каком языке будет послан запрос
    request.session_id = 'small-talk-bfkbhc' # ID Сессии диалога (нужно, чтобы потом учить бота)
    request.query = update.message.text # Посылаем запрос к ИИ с сообщением от юзера
    responseJson = json.loads(request.getresponse().read().decode('utf-8'))
    response = responseJson['result']['fulfillment']['speech'] # Разбираем JSON и вытаскиваем ответ
    # Если есть ответ от бота - присылаем юзеру, если нет - бот его не понял
    if response:
        context.bot.send_message(chat_id=update.effective_chat.id, text=response)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='Я Вас не совсем понял!')

def main():
    updater = Updater(token='982560961:AAHERlYwllDeXwdv-rXwdwj0NyazSsXC27Q', use_context=True)
    dispatcher = updater.dispatcher
    text_message_handler = MessageHandler(Filters.text, textMessage)
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    ask_handler = CommandHandler('ask', ask)
    dispatcher.add_handler(ask_handler)
    roll_handler = CommandHandler('roll', roll)
    dispatcher.add_handler(roll_handler)
    dispatcher.add_handler(text_message_handler)
    updater.start_polling()
    print('shit is going down')
    updater.idle()

if __name__ == '__main__':
    main()
