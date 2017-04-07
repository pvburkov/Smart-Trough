from datetime import datetime
import sqlalchemy
import unittest

class DBWorker():
    """
    класс для работы с базой данных
    поля: дата/время, температура, атмосферное давление, влажность воздуха
    """
    
    def __init__(self, **kwargs):
        """
        конструктор класса DBWorker
        """
        self.datetime_point = datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M:%S")
        self.temperature = kwargs['temperature']
        self.pressure = kwargs['pressure']
        self.humidity = kwargs['humidity']
        self.photo_path = kwargs['photo_path']

    def db_insert_data(self):
        """
        метод класса DBWorker: записывает информацию из полей класса в БД
        """
        pass

# end DBWorker description

class Test_DBWorker(unittest.TestCase):
    """
    тест для проверки корректности приходящих данных
    """
    def test_make_worker(self):
        db = DBWorker(temperature = 13, pressure = 760, humidity = 80, photo_path = r'photo.jpeg')
        self.assertEqual(db.temperature, 13)
        self.assertEqual(db.humidity, 80)
        self.assertEqual(type(db.photo_path), str)

# end Test_DBWorker description

if __name__ == '__main__':
    unittest.main()