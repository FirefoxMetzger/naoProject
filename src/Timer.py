# -- NAO Project Timer file --
# License: GPL
# Author: Sebastian Wallkoetter
# Email: sebastian@wallkoetter.net
#
# This file allows the NAO to report the current time and date. Further,
# NAO can be asked to set a timer. It will notify when the timers runs out.

from datetime import datetime

from naoqi import ALBroker
from naoqi import ALProxy


class Timer:
    def __init__(self, broker):
        self.tts = ALProxy("ALMemory")

    def getTime(self):
        ROUND_TO_MULTIPLE = 5
        
        hour = datetime.now().hour
        minute = datetime.now().minute

        # round to the nearest multiple for nice numbers
        fraction = minute % ROUND_TO_MULTIPLE
        if fraction > ROUND_TO_MULTIPLE / 2:
            # round up
            minute = minute + (ROUND_TO_MULTIPLE - fraction)
        else:
            # round down
            minute = minute - fraction

        return "It's about %02d:%02d" % (hour, minute)
        

    def getDate(self):
        day_name = datetime.now().weekday
        date = datetime.now().date
        month = datetime.now().month
        
        return "Today is %s, %s of %s" % (day_name, date, month)

    def setTimer(self):
        pass

    
