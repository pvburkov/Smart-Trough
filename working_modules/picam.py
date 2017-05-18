import picamera
import time
import os

rec_path = '/home/pi/dev_trough/photo'


class PiCam(picamera.PiCamera):
    def __init__(self):
        super().__init__()
        self.resolution = (1024, 768)
        self.start_preview()
        time.sleep(2)

    @staticmethod
    def directory(way):
        if not os.path.exists(way):
            os.makedirs(way)
        return way

    def take_photo(self, dt_photo):
        path = rec_path + '/' + dt_photo.strftime('%d_%m_%Y')
        self.directory(path)
        photo_path = path + '/' + dt_photo.strftime('%H_%M') + '.jpg'
        self.capture(photo_path)
        return path
