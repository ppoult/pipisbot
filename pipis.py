import vk_api
from telegram.ext import Updater, CommandHandler
import requests
import re
import json
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

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
    response_two = response['items'][0]['text']
    response_three = response['items'][0]['attachments'][0]['photo']['sizes'][7]
    return response_two
    return response_three

def GetPic(): #сгребаем картинку со стены Pipis

    login, password = 'flokinokinihilipilifications@mail.ru', 'WSK741qaz'
    vk_session = vk_api.VkApi(login, password)

    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    vk = vk_session.get_api()

    response = vk.wall.get(domain='pipis_everyday', count=1)  # Используем метод wall.get
    response_three = response['items'][0]['attachments'][0]['photo']['sizes'][7]['url']
    return response_three



def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Привет. Я — Пипис, полиморфный цыпленок. Могу подскзать, какой сегодня день.')

def ask(update, context):
    answer = GetShit()
    pic = GetPic()
    context.bot.send_message(chat_id=update.effective_chat.id, text='Бакаа, бкааа...бкаа, бка')
    context.bot.send_message(chat_id=update.effective_chat.id, text=answer)
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=pic)

def main():
    updater = Updater(token='982560961:AAHERlYwllDeXwdv-rXwdwj0NyazSsXC27Q', use_context=True)
    dispatcher = updater.dispatcher
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    ask_handler = CommandHandler('ask', ask)
    dispatcher.add_handler(ask_handler)
    updater.start_polling()
    print('shit is going down')
    updater.idle()

if __name__ == '__main__':
    main()
