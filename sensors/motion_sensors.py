import RPi.GPIO as GPIO
from datetime import datetime


class HC_SR501:
    """"HC_SR501 motion sensor reader states class for Raspberry"""
    state = None

    def __init__(self, pin):
        self.pin = pin
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin, GPIO.IN)

    @property
    def is_motion(self):
        self.state = GPIO.input(self.pin)
        return self.state
