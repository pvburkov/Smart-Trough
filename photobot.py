import os
import os.path
import random
import telebot
import time
import unittest

class PhotoBot():
    """
    класс, отвечающий за загрузку фотографий в чат-бот Telegram
    поля: название бота, логин, пароль (возможны изменения), путь к файлу с фото
    """

    def __init__(self, **kwargs):
        """
        конструктор класса PhotoBot
        название бота, логин и пароль являются параметрами по умолчанию
        """
        self.token = kwargs['token']
        self.channel_name = kwargs['channel_name']
        self.photo_dir = kwargs['photo_dir']

    def push_photo(self):
        """
        метод класса PhotoBot, который загружает фотографию в чат-бот Telegram
        """
        bot = telebot.TeleBot(self.token)
        
        @bot.message_handler(commands = ['start'])
        def handle_start(message):
            bot.send_message(message.chat.id, 'Hello! Funny birds are greeting you here!')

        @bot.message_handler(commands = ['new'])
        def handle_new(message):
            new_file_time = 0
            for file in os.listdir(self.photo_dir):
                file_path = self.photo_dir + '\\' + file
                if file.split('.')[1] == 'jpg' and os.path.getmtime(file_path) > new_file_time:
                    new_file = file_path
                    new_file_time = os.path.getmtime(file_path)
            photo = open(new_file, 'rb')
            bot.send_photo(message.chat.id, photo)
            photo.close()

        @bot.message_handler(commands = ['old'])
        def handle_old(message):
            old_file_time = 20000000000
            for file in os.listdir(self.photo_dir):
                file_path = self.photo_dir + '\\' + file
                if file.split('.')[1] == 'jpg' and os.path.getmtime(file_path) < old_file_time:
                    old_file = file_path
                    old_file_time = os.path.getmtime(file_path)
            photo = open(old_file, 'rb')
            bot.send_photo(message.chat.id, photo)
            photo.close()

        @bot.message_handler(commands = ['random'])
        def handle_random(message):
            while True:
                rand_file = random.choice(os.listdir(self.photo_dir))
                if rand_file.split('.')[1] == 'jpg':
                    break
            photo = open(self.photo_dir + '\\' + rand_file, 'rb')
            bot.send_photo(message.chat.id, photo)
            photo.close()

        @bot.message_handler(commands = ['hour'])
        def handle_hour(message):
            timestamp = time.time()
            for file in os.listdir(self.photo_dir):
                file_path = self.photo_dir + '\\' + file
                if file.split('.')[1] == 'jpg' and timestamp - os.path.getmtime(file_path) < 3600:
                    photo = open(file_path, 'rb')
                    bot.send_photo(message.chat.id, photo)
                    photo.close()

        @bot.message_handler(content_types=["text"])
        def handle_message(message):
            bot.send_message(message.chat.id, 'Tweet! Tweet-tweet! Tweet!')
        
        bot.polling(none_stop=True)

class Test_PhotoBot(unittest.TestCase):
    """
    тест для отработки прихода фото и отправки его в Телеграм
    """
    def test_make_bot(self):
        pb = PhotoBot(photo_dir = r'C:\\Users\\ASUS\\Desktop\\space', 
                        channel_name = '@TroughTestBot', 
                        token = '301887493:AAFdNXpQbbw_90cS8Ai7qfuquxejKILicZk')
        self.assertEqual(pb.channel_name, '@TroughTestBot')
        self.assertTrue(pb.push_photo())

# end Test_PhotoBot description

if __name__ == '__main__':
    unittest.main()

