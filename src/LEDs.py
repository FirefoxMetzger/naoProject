# -*- encoding UTF-8 -*-

import sys
import math
from time import sleep
from naoqi import ALProxy

from NaoModule import NaoModule


class LEDs(NaoModule):

    def __init__(self, name):
        NaoModule.__init__(self, name)

        self.getHandle("parameter_server", True)
        self.getHandle("ALLeds", True)
        
        #refactor me
        if self.hasHandle("parameter_server"):
            self.params = self.handles["parameter_server"]

        if self.hasHandle("ALLeds"):
            self.leds = self.handles["ALLeds"]
        else:
            logger.info("This module will not do anything.")
        
        self.set_eyes('w')
        self.eyes_on()

    def ears_on(self):
        """ turn the ears off """
        self.leds.on("EarLeds")

    def ears_off(self):
        """ turn the ears on """
        self.leds.off("EarLeds")

    def spin_ears(self, delay=0.2):
        """ spin the ears once """
        ears = self.params.getParameter("leds", "ears")
        for pos in ears:
            left = "Ears/Led/Left/" + pos + "/Actuator/Value"
            right = "Ears/Led/Right/" + pos + "/Actuator/Value"
            self.leds.createGroup("ear", [left, right])
            self.leds.on("ear")
            sleep(delay)
            self.leds.off("ear")

    def set_eyes(self, col='w'):
        """ set the eye color """
        colors = get_color_list(col)
        bottom_eye = self.params.getParameter("leds", "bottom_eye")
        lower_eye = self.params.getParameter("leds", "lower_eye")
        middle_eye = self.params.getParameter("leds", "middle_eye")
        upper_eye = self.params.getParameter("leds", "upper_eye")
        top_eye = self.params.getParameter("leds", "top_eye")
        bottom = []
        lower = []
        middle = []
        upper = []
        top = []
        eyes = []
        for led in bottom_eye:
            for col in colors:
                bottom.append("Face/Led/" + col + "/" + led + "/Actuator/Value")
                eyes.append("Face/Led/" + col + "/" + led + "/Actuator/Value")
        for led in lower_eye:
            for col in colors:
                lower.append("Face/Led/" + col + "/" + led + "/Actuator/Value")
                eyes.append("Face/Led/" + col + "/" + led + "/Actuator/Value")
        for led in middle_eye:
            for col in colors:
                middle.append("Face/Led/" + col + "/" + led + "/Actuator/Value")
                eyes.append("Face/Led/" + col + "/" + led + "/Actuator/Value")
        for led in upper_eye:
            for col in colors:
                upper.append("Face/Led/" + col + "/" + led + "/Actuator/Value")
                eyes.append("Face/Led/" + col + "/" + led + "/Actuator/Value")
        for led in top_eye:
            for col in colors:
                top.append("Face/Led/" + col + "/" + led + "/Actuator/Value")
                eyes.append("Face/Led/" + col + "/" + led + "/Actuator/Value")
        self.leds.createGroup("Eyes", eyes)
        self.leds.createGroup("Top", top)
        self.leds.createGroup("Upper", upper)
        self.leds.createGroup("Middle", middle)
        self.leds.createGroup("Lower", lower)
        self.leds.createGroup("Bottom", bottom)

    def eyes_on(self):
        """ turn eyes on """
        self.eyes_off()
        self.leds.on("Eyes")

    def eyes_off(self):
        """ turn eyes off """
        self.leds.off("FaceLeds")

    def blink(self, time=0.6):
        """ Make the robot blink """
        self.close_eyes(2.0 * time / 5.0)
        sleep(time / 5.0)
        self.open_eyes(2.0 * time / 5.0)

    def open_eyes(self, time=0.3):
        self.leds.on("Middle")
        sleep(time / 2.0)
        self.leds.on("Upper")
        self.leds.on("Lower")
        sleep(time / 2.0)
        self.leds.on("Bottom")
        self.leds.on("Top")

    def close_eyes(self, time=0.3):
        self.leds.off("Top")
        self.leds.off("Bottom")
        sleep(time / 2.0)
        self.leds.off("Upper")
        self.leds.off("Lower")
        sleep(time / 2.0)
        self.leds.off("Middle")


def get_color_list(col):
    if col == 'b':
        colors = ["Blue"]
    elif col == 'r':
        colors = ["Red"]
    elif col == 'g':
        colors = ["Green"]
    elif col == 't':
        colors = ["Blue", "Green"]
    elif col == 'y':
        colors = ["Red", "Green"]
    elif col == 'p':
        colors = ["Red", "Blue"]
    else:
        colors = ["Blue", "Green", "Red"]
    return colors
