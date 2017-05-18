from sensors import th_sensors as th, pressure_sensors as ps, motion_sensors as ms
from works import picam
from datetime import datetime

TH_PIN = 7
MS_PIN = 13

motion_flag = 1

th_sensor = th.DHT11(TH_PIN)
pressure_sensor = ps.LPS331()
motion_sensor = ms.HC_SR501(MS_PIN)
camera = picam.PiCam()

while 1:
    if motion_sensor.is_motion & motion_flag:
        date_motion = datetime.now()
        photo_path = camera.take_photo(date_motion)
        # Отправить в телеграм-бот фотографию которая находится по photo_path
        pressure_sensor.read()
        th_sensor.read()
        temperature = pressure_sensor.temperature
        humidity = th_sensor.humidity
        pressure = pressure_sensor.pressure
        print('T = ', temperature,'Hum = ',humidity, 'Press = ', pressure, 'Date = ', date_motion)
        # Занести в БД temperature, humidity, pressure, date_motion, photo_path
        motion_flag = 0
    if not motion_sensor.is_motion:
        motion_flag = 1
