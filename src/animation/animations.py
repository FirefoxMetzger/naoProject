# -*- encoding UTF-8 -*-

import sys
import math
from time import sleep
from naoqi import ALProxy
from naoqi import ALModule


class Animations(ALModule):

    def __init__(self, name):
        ALModule.__init__(self, name)
        try:
            self.motion = ALProxy("ALMotion")
        except Exception, error:
            print "Could not create proxy to ALMotion"
            print "Error was: ", error
            sys.exit(1)

    def __enter__(self):
        return self

    def __exit__(self, exec_type, exec_value, traceback):
        return