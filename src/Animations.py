# -*- encoding UTF-8 -*-

import sys
import math
from time import sleep

from NaoModule import NaoModule


class Animations(NaoModule):

    def __init__(self, name):
        NaoModule.__init__(self, name)

        self.getHandle("ALMotion")
