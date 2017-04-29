import os
import timer.fuzzy_time as date
import time

from NaoModule import NaoModule

class TimerModule(NaoModule):
    """ A class to fullfill basic requirements for AINT512

    """

    # -------------------------------------
    # Setup Module
    # -------------------------------------

    def __init__(self,name, is_on_robot):
        NaoModule.__init__(self, name)
        self.on_robot = is_on_robot
        
        # get Proxy Handles
        self.getHandle("ALMemory")
        self.getHandle("ALTextToSpeech")
        self.getHandle("speech_module")

        # setup Proxy dependant stuff
        self.loadMenuTopic()

    def loadMenuTopic(self):   
        rel_dir = ['topics', 'timer_menu.top']
        if self.on_robot:
            base_dir = "/home/nao/naoProject"
            path = self.getAbsPath(rel_dir, base_dir)
        else:
            path = self.getAbsPath(rel_dir)
            
        if self.hasHandle("speech_module"):
            self.handles["speech_module"].addMenuTopic(path)
        else:
            self.logger.debug("No Speech Topic.")

    # -------------------------------------
    # Callbacks
    # -------------------------------------
    
    def setTimerCallback(self, eventName, seconds):
        """ Set a timer """
        self.logger.debug("Setting a timer for %s seconds." % seconds)
        seconds = float(seconds)
        time.sleep(seconds)
        
        say_string = "The time is up. " + str(seconds) + " seconds have passed."

        self.handles["ALTextToSpeech"].say(say_string)
        print(say_string)

    def sayDateCallback(self, unused_value):
        """ Say the date"""
        self.logger.debug("Saying Date")
        
        now = date.dateAndTime(False,True)
        say_string = "Today is " + str(now) 
        self.handles["ALTextToSpeech"].say(str(say_string))

    def sayTimeCallback(self, unused_value):
        """ Say the time"""
        self.logger.debug("Saying current time.")
        
        now = date.dateAndTime(True,False)
        say_string = "It is " + str(now) 
        self.handles["ALTextToSpeech"].say(str(say_string))

    def sayDateAndTime(self):
        """ Say the Date and Time """
        self.logger.debug("Saying time and date.")
        
        now = date.dateAndTime()
        say_string = "It is " + str(now)
        self.handles["ALTextToSpeech"].say(str(say_string))

    # -------------------------------------
    # Overwritten from NaoModule
    # -------------------------------------

    def __enter__(self):
        if self.hasHandle("ALMemory"):
            memory = self.handles["ALMemory"]
            memory.subscribeToEvent("sayDate", self.name, "sayDateCallback")
            memory.subscribeToEvent("sayTime", self.name, "sayTimeCallback")
            memory.subscribeToEvent("setTimer", self.name, "setTimerCallback")
        else:
            self.logger.debug("Could not unsubscribe Events.")

        return self

    def __exit__(self, exec_type, exec_value, traceback):
        if self.hasHandle("ALMemory"):
            memory = self.handles["ALMemory"]
            memory.unsubscribeToEvent("sayDate", self.name)
            memory.unsubscribeToEvent("sayTime", self.name)
            memory.unsubscribeToEvent("setTimer", self.name)
        else:
            self.logger.debug("Could not unsubscribe Events.")
