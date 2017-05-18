from datetime import datetime
from time import time
import config
import os
import os.path
import random
import telebot
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

def photobot_work(photo_dir):
    """
    Функция, загружающая фотографии в чат-бот Telegram.
    In: директория с фотографиями
    """
    bot = telebot.TeleBot(config.BOT_TOKEN)

    class WebhookServer(object):
        @cherrypy.expose
        def index(self):
            if 'content-length' in cherrypy.request.headers and \
                            'content-type' in cherrypy.request.headers and \
                            cherrypy.request.headers['content-type'] == 'application/json':
                length = int(cherrypy.request.headers['content-length'])
                json_string = cherrypy.request.body.read(length).decode("utf-8")
                update = telebot.types.Update.de_json(json_string)
                # Эта функция обеспечивает проверку входящего сообщения
                bot.process_new_updates([update])
                return ''
            else:
                raise cherrypy.HTTPError(403)
    
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
        timestamp = time()
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

    # (пере)запуск вебхука
    bot.remove_webhook()
    bot.set_webhook(url = config.WEBHOOK_URL_BASE + config.WEBHOOK_URL_PATH,
                    certificate = open(config.WEBHOOK_SSL_CERT, 'r'))
    
    # настройки сервера CherryPy
    cherrypy.config.update({
        'server.socket_host': config.WEBHOOK_LISTEN,
        'server.socket_port': config.WEBHOOK_PORT,
        'server.ssl_module': 'builtin',
        'server.ssl_certificate': config.WEBHOOK_SSL_CERT,
        'server.ssl_private_key': config.WEBHOOK_SSL_PRIV
    })

    cherrypy.quickstart(WebhookServer(), config.WEBHOOK_URL_PATH, {'/': {}})

if __name__ == '__main__':
    try:
        photobot_work(os.getcwd())
    except Exception as e:
        logger(e)
