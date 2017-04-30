import os
import timer.fuzzy_time as date
import time
import re

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
            pass
        else:
            self.logger.debug("No Speech Topic.")

    # -------------------------------------
    # Callbacks
    # -------------------------------------
    
    def setTimerCallback(self, eventName, time_string):
        """ Set a timer """
        self.logger.debug("Setting a timer.")
        stop_time = 0 # in s

        time_string = time_string.replace("set a timer for","")

        # get rid of spoken fractions
        fractions = dict()
        fractions["half"] = 0.5
        fractions["halfs"] = 0.5
        fractions["quarter"] = 0.25
        fractions["quarters"] = 0.25
        fractions["third"] = 1/3.0
        fractions["thirds"] = 1/3.0

        time_indicators = dict()
        time_indicators["day"] = 24 * 60*60.0
        time_indicators["days"] = 24 * 60*60.0
        time_indicators["hour"] = 60*60.0
        time_indicators["hours"] = 60*60.0
        time_indicators["minute"] = 60.0
        time_indicators["minutes"] = 60.0
        time_indicators["second"] = 1.0
        time_indicators["seconds"] = 1.0

        unknown_total = 0.0
        current_value = 0.0
        current_fraction = 1.0
        of_flag = False
        for word in time_string.split():
            try:
                current_value += float(word)
            except ValueError:
                # not a number
                if word in ["an", "a"]:
                    if not of_flag:
                        current_value += 1
                elif word == "of":
                    of_flag = True
                elif word in fractions.keys():
                    current_fraction *= fractions[word]
                elif word in time_indicators.keys():
                    unknown_total += current_value * current_fraction
                    stop_time += unknown_total * time_indicators[word]

                    unknown_total = 0
                    current_value = 0
                    current_fraction = 1.0
                    of_flag = False
                elif word == "and":
                    unknown_total += current_value * current_fraction
                    current_value = 0
                    current_fraction = 1.0

        split = stop_time
        seconds = stop_time % 60
        minutes = stop_time // 60 % 60
        hours = stop_time // (60 ** 2) % 24
        days = stop_time // (60 ** 2 * 24)

        sec = stop_time % 60

        self.logger.debug("Timer for %f seconds set." % stop_time)
        time.sleep(stop_time)

        # a bit hacky
        self.handles["ALMemory"].raiseEvent("timerSeconds", seconds)
        self.handles["ALMemory"].raiseEvent("timerMinutes", minutes)
        self.handles["ALMemory"].raiseEvent("timerHours", hours)
        self.handles["ALMemory"].raiseEvent("timerDays", days)
        self.handles["ALMemory"].raiseEvent("timerUp", stop_time)

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
