#!/usr/bin/env python3

# pylint: disable=no-member

import time
import RPi.GPIO as GPIO
from config import *  # pylint: disable=unused-wildcard-import
import neopixel
import board
import busio
import w1thermsensor
import adafruit_bme280.advanced as adafruit_bme280
from mfrc522 import MFRC522
from datetime import datetime
from mqtt_client import MyMQTTClient


def format_time(time):
    return time.strftime("%H:%M:%S")


class LedController:
    def __init__(self, brightness=1.0 / 32, auto_write=False):
        self.pixels = neopixel.NeoPixel(my_board.D18, 8, brightness=brightness, auto_write=auto_write)

    def set_color(self, color):
        self.pixels.fill(color)
        self.pixels.show()

    def clear(self):
        self.pixels.fill((0, 0, 0))
        self.pixels.show()

    def set_raibow(self):
        self.pixels[0] = (255, 0, 0)
        self.pixels[1] = (0, 255, 0)
        self.pixels[2] = (0, 0, 255)
        self.pixels[3] = (255, 255, 0)
        self.pixels[4] = (0, 255, 255)
        self.pixels[5] = (255, 0, 255)
        self.pixels[6] = (255, 255, 255)
        self.pixels[7] = (63, 63, 63)
        self.pixels.show()


class RFIDController:
    def __init__(self):
        self.mfrc522_reader = MFRC522()
        self.last_time = datetime.now()
        self.is_being_used = False

    def read(self, mqtt_client: MyMQTTClient):
        (status, TagType) = self.mfrc522_reader.MFRC522_Request(self.mfrc522_reader.PICC_REQIDL)
        if status == self.mfrc522_reader.MI_OK:
            (status, uid) = self.mfrc522_reader.MFRC522_Anticoll()

            if status == self.mfrc522_reader.MI_OK:
                num = 0
                for i in range(0, len(uid)):
                    num += uid[i] << (i * 8)

                new_time = datetime.now()

                if (new_time - self.last_time).seconds > 0.6:
                    # print("delta more than 1 sec")
                    self.last_time = new_time
                    self.is_being_used = True
                    mqtt_client.odbicie(str(num))
                    return True

                self.last_time = new_time
                self.is_being_used = False

            else:
                self.is_being_used = False
        else:
            self.is_being_used = False
        return False

    def get_info(self):
        print(f"Last time: {format_time(self.last_time)}")


class Test:
    def __init__(self, mqtt_client):
        self.led_controller = LedController()
        self.rfid_controller = RFIDController()
        self.time_period = 0.5
        self.mqtt_client = mqtt_client

    def buzzer(self, state):
        GPIO.output(buzzerPin, not state)

    def run(self):
        was_read_successful = self.rfid_controller.read(self.mqtt_client)
        if was_read_successful:
            self.rfid_controller.get_info()
            self.buzzer(True)
            self.led_controller.set_raibow()

        if (self.rfid_controller.last_time != None):
            diff = datetime.now() - self.rfid_controller.last_time
            if diff.seconds >= self.time_period:
                self.buzzer(False)
                self.led_controller.clear()

        if not self.rfid_controller.is_being_used:
            self.led_controller.clear()
            self.buzzer(False)


def on_get_response_callback(response):
    print(f"WILL BE DISPLAYED ---> || {response} ||")


if __name__ == "__main__":
    my_mqtt_client = MyMQTTClient(on_get_response=on_get_response_callback)

    test = Test(my_mqtt_client)
    while True:
        test.run()
        time.sleep(0.1)
