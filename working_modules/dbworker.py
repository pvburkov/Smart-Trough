from datetime import datetime
import sqlite3 as lite
import unittest

def db_logger(error):
    log = open('db_errors.log', 'w')
    out = datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M:%S")
    out += ' : Error ' + str(error)
    log.close()

class DBWorker():
    """
    класс для работы с базой данных
    поля: дата/время, температура, атмосферное давление, влажность воздуха
    """
    
    def __init__(self, dbname):
        """
        конструктор класса DBWorker
        """
        self.datetime_point = datetime.strftime(datetime.now(), "%Y.%m.%dT%H:%M:%S")
        self.dbname = dbname

    def db_insert_data(self, temperature, pressure, humidity, photo_path):
        """
        метод класса DBWorker: записывает информацию из полей класса в БД
        """
        try:
            dbcon = lite.connect(self.dbname)
        except lite.DatabaseError:
            db_logger(lite.DatabaseError)
            return lite.DatabaseError
        
        with dbcon:
            cur = dbcon.cursor()
            query = 'CREATE TABLE IF NOT EXISTS TroughInfo(ID INTEGER PRIMARY KEY, ' 
            query += 'DateTime TEXT, Temperature INTEGER, Pressure INTEGER, '
            query += 'Humidity INTEGER, PhotoPath TEXT);'
            cur.execute(query)
            query2 = 'INSERT INTO TroughInfo(DateTime, Temperature, Pressure, Humidity, PhotoPath) VALUES(?,?,?,?,?);'
            cur.execute(query2, (self.datetime_point, temperature, pressure, humidity, photo_path))
        
        dbcon.close()
        return True

    def db_get_all_data(self):
        """
        метод класса DBWorker: выводит на экран всю информацию из БД
        """
        try:
            dbcon = lite.connect(self.dbname)
        except lite.DatabaseError:
            db_logger(lite.DatabaseError)
            return lite.DatabaseError
 
        with dbcon:    
            cur = dbcon.cursor()    
            cur.execute("SELECT * FROM TroughInfo")
            rows = cur.fetchall()
        
            for row in rows:
                print(row)
        
        dbcon.close()
        return True

# end DBWorker description

class Test_DBWorker(unittest.TestCase):
    """
    тест для проверки корректности приходящих данных
    """
    def test_make_worker(self):
        db = DBWorker(dbname = 'testdb.db')
        self.assertEqual(type(db.dbname), str)

        self.assertTrue(db.db_insert_data(temperature = 13, pressure = 760, humidity = 80, photo_path = r'photo.jpeg'))
        self.assertTrue(db.db_get_all_data())

# end Test_DBWorker description

if __name__ == '__main__':
    unittest.main()