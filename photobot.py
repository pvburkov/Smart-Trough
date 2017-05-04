import telebot

class PhotoBot():
    """
    класс, отвечающий за загрузку фотографий в чат-бот Telegram
    поля: название бота, логин, пароль (возможны изменения), путь к файлу с фото
    """

    def __init__(self, photo_path):
        """
        конструктор класса PhotoBot
        название бота, логин и пароль являются параметрами по умолчанию
        """
        self.botname = 'FunnyBirds'
        self.login = 'admin'
        self.password = 'parole'
        self.photo_path = photo_path

    def push_photo(self):
        """
        метод класса PhotoBot, который загружает фотографию в чат-бот Telegram
        """
        pass

	#simple comment