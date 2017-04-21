
import fuzzy_time as date
import time

from naoqi import ALProxy
from naoqi import ALModule

class TimerModule(ALModule):
    """ A class to fullfill basic requirements for AINT512

    """
    def __init__(self,name):
        ALModule.__init__(self, name)
        self.name = name

        self.memory = ALProxy("ALMemory")
        self.tts = ALProxy("ALTextToSpeech")
        self.speech = ALProxy("speech_module")

        self.speech.addMenuTopic("/home/firefoxmetzger/Documents/naoProject/src/timer/timer_menu.top")

        self.memory.subscribeToEvent("sayDate", self.name, "sayDateCallback")
        self.memory.subscribeToEvent("sayTime", self.name, "sayTimeCallback")
        self.memory.subscribeToEvent("setTimer", self.name, "setTimerCallback")

    def __enter__(self):
        return self

    def __exit__(self, exec_type, exec_value, traceback):
        return

    def setTimerCallback(self, eventName, seconds):
        """ Comment to bind method

        """
        seconds = float(seconds)
        time.sleep(seconds)
        
        say_string = "The time is up. " + str(seconds) + " seconds have passed."

        self.tts.say(say_string)
        print(say_string)


    def sayDateCallback(self, unused_value):
        """ Comment to bind method

        """
        now = date.dateAndTime(False,True)
        say_string = "Today is " + str(now) 
        self.tts.say(str(say_string))
        print(say_string)

    def sayTimeCallback(self, unused_value):
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
