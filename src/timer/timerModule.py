
import fuzzy_time as date
import time

from naoqi import ALProxy
from naoqi import ALModule

class TimerModule(ALModule):
    """ A class to fullfill basic requirements for AINT512

    """
    def __init__(self,name):
        ALModule.__init__(self, name)
        self.tts = ALProxy("ALTextToSpeech")

    def setTimer(self, seconds):
        """ Comment to bind method

        """
        time.sleep(seconds)
        self.tts.say("The time is up.")
        self.tts.say(str(seconds) + " seconds have passed.")
        print(str(seconds) + " seconds timer has ended.")


    def sayDate(self):
        """ Comment to bind method

        """
        now = date.dateAndTime(False,True)
        say_string = "Today is " + str(now) 
        self.tts.say(str(say_string))
        print(say_string)

    def sayTime(self):
        """ Comment to bind method
        
        """
        now = date.dateAndTime(True,False)
        say_string = "It is " + str(now) 
        self.tts.say(str(say_string))
        print(say_string)

    def sayDateAndTime(self):
        """ Comment to bind method

        """
        now = date.dateAndTime()
        say_string = ("It is " + str(now))
        self.tts.say(str(say_string))
        print(say_string)
