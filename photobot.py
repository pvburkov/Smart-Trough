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
    WEBHOOK_HOST = '52.169.114.1'
    WEBHOOK_PORT = 443  
    WEBHOOK_LISTEN = '0.0.0.0'  # На некоторых серверах придется указывать такой же IP, что и выше

    WEBHOOK_SSL_CERT = './webhook_cert.pem'  # Путь к сертификату
    WEBHOOK_SSL_PRIV = './webhook_pkey.pem'  # Путь к приватному ключу

    WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
    WEBHOOK_URL_PATH = "/%s/" % (token)

    bot = telebot.TeleBot(token)

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

    # снятие вебхука перед повторной установкой (избавляет от некоторых проблем)
    bot.remove_webhook()
    bot.set_webhook(url = WEBHOOK_URL_BASE + WEBHOOK_URL_PATH,
                    certificate = open(WEBHOOK_SSL_CERT, 'r'))
    
    # настройки сервера CherryPy
    cherrypy.config.update({
        'server.socket_host': WEBHOOK_LISTEN,
        'server.socket_port': WEBHOOK_PORT,
        'server.ssl_module': 'builtin',
        'server.ssl_certificate': WEBHOOK_SSL_CERT,
        'server.ssl_private_key': WEBHOOK_SSL_PRIV
    })

    cherrypy.quickstart(WebhookServer(), WEBHOOK_URL_PATH, {'/': {}})

if __name__ == '__main__':
    photobot_work_v2('301887493:AAFdNXpQbbw_90cS8Ai7qfuquxejKILicZk', os.getcwd())