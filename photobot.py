from datetime import datetime
import os
import os.path
import random
import telebot
import time
import unittest 

def logger(error):
    """
    Функция, работающая с журналом ошибок (лог-файлом)
    """
    log = open('telegram_errors.log', 'a')
    out = datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M:%S")
    out += ' : Error ' + str(error) + '\n'
    log.close()

def fpath(fdir, fname):
    return fdir + '/' + fname

def photobot_work(token, photo_dir):
    """
    Функция, загружающая фотографии в чат-бот Telegram.
    In: токен для доступа в чат-бот, директория с фотографиями
    """
    bot = telebot.TeleBot(token)
    
    @bot.message_handler(commands = ['start'])
    def handle_start(message):
        bot.send_message(message.chat.id, 'Hello! Funny birds are greeting you here!')

    @bot.message_handler(commands = ['new'])
    def handle_new(message):
        new_file_time = 0
        for file in os.listdir(photo_dir):
            file_path = fpath(photo_dir, file)
            if os.path.isfile(file_path):
                if file.split('.')[1] == 'jpg' and os.path.getmtime(file_path) > new_file_time:
                    new_file = file_path
                    new_file_time = os.path.getmtime(file_path)
        photo = open(new_file, 'rb')
        bot.send_photo(message.chat.id, photo)
        photo.close()

    @bot.message_handler(commands = ['old'])
    def handle_old(message):
        old_file_time = 20000000000
        for file in os.listdir(photo_dir):
            file_path = fpath(photo_dir, file)
            if os.path.isfile(file_path):
                if file.split('.')[1] == 'jpg' and os.path.getmtime(file_path) < old_file_time:
                    old_file = file_path
                    old_file_time = os.path.getmtime(file_path)
        photo = open(old_file, 'rb')
        bot.send_photo(message.chat.id, photo)
        photo.close()

    @bot.message_handler(commands = ['random'])
    def handle_random(message):
        while True:
            rand_file = random.choice(os.listdir(photo_dir))
            if os.path.isfile(rand_file):    
                if rand_file.split('.')[1] == 'jpg':
                    break
        photo = open(fpath(photo_dir, rand_file), 'rb')
        bot.send_photo(message.chat.id, photo)
        photo.close()

    @bot.message_handler(commands = ['hour'])
    def handle_hour(message):
        timestamp = time.time()
        for file in os.listdir(photo_dir):
            file_path = fpath(photo_dir, file)
            if os.path.isfile(file_path):
                if file.split('.')[1] == 'jpg' and timestamp - os.path.getmtime(file_path) < 3600:
                    photo = open(file_path, 'rb')
                    bot.send_photo(message.chat.id, photo)
                    photo.close()

    @bot.message_handler(content_types=["text"])
    def handle_message(message):
        bot.send_message(message.chat.id, 'Tweet! Tweet-tweet! Tweet!')

    while True:
        try:
            bot.polling(none_stop=True)
        except ConnectionResetError:
            logger(ConnectionResetError)
            time.sleep(3)

if __name__ == '__main__':
    photobot_work('301887493:AAFdNXpQbbw_90cS8Ai7qfuquxejKILicZk', os.getcwd())
