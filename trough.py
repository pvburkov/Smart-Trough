#!/usr/bin/env python3
from sensors import th_sensors as th, pressure_sensors as ps, motion_sensors as ms
from working_modules import picam, photo_sender, dbworker
from datetime import datetime
import time

TH_PIN = 7
MS_PIN = 13

DBNAME = 'through.db'

motion_flag = 1

th_sensor = th.DHT11(TH_PIN)
pressure_sensor = ps.LPS331()
motion_sensor = ms.HC_SR501(MS_PIN)
camera = picam.PiCam()

while 1:
    if motion_sensor.is_motion & motion_flag:
        date_motion = datetime.now()
        photo_path = camera.take_photo(date_motion)
        photo_sender.send_photo(photo_path)
        pressure_sensor.read()
        th_sensor.read()
        temperature = pressure_sensor.temperature
        humidity = th_sensor.humidity
        pressure = pressure_sensor.pressure
        print('T = ', temperature,'Hum = ',humidity, 'Press = ', pressure, 'Date = ', date_motion)
        db = dbworker.DBWorker(DBNAME)
        db.db_insert_data(temperature,pressure, humidity, photo_path)
        motion_flag = 0
        time.sleep(3)
    if not motion_sensor.is_motion:
        motion_flag = 1
