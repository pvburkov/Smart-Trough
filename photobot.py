import telebot
import os
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
        tb = telebot.TeleBot(self.token)
        
        @tb.message_handler(content_types=["text"])
        def photo_for_message(message):
            for file in os.listdir(self.photo_dir):
                if file.split('.')[1] == 'jpg':
                    photo = open(self.photo_dir + '\\' + file, 'rb')
                    tb.send_photo(message.chat.id, photo)
                    photo.close()
        
        tb.polling(none_stop=True)

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
