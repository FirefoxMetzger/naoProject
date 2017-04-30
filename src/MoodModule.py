import random
import time

from NaoModule import NaoModule

class MoodModule(NaoModule):
    
    # -------------------------------------
    # Setup Module
    # -------------------------------------
    
    def __init__(self, name):
        NaoModule.__init__(self, name)

        self.handles = dict()

        # get Proxies
        self.getHandle("ALMemory", True)
        self.getHandle("ALMotion")
        self.getHandle("leds")
        self.getHandle("ALBasicAwareness")
        self.getHandle("ALSpeechRecognition")

        #setup proxy dependant stuff
        self.setupMemory()
        self.setupASR()
        self.setupBasicAwareness()
        
        self.blink_frequency = 500 #ms
        self.is_blinking = True

    def setupMemory(self):
        if self.hasHandle("ALMemory"):
            memory = self.handles["ALMemory"]
            memory.subscribeToEvent("emoBlink", self.name, "blinkingCallback")
            memory.subscribeToEvent("ALSpeechRecognition/Status", self.name,\
                                     "SpeechStatusCallback")
            memory.subscribeToEvent("WordRecognized", self.name, "WordRecognizedCallback")
        else:
            self.logger.debug("Not setting up any callbacks")

    def setupBasicAwareness(self):
        if self.hasHandle("ALBasicAwareness"):
            baware = self.handles["ALBasicAwareness"]
            baware.setEngagementMode("FullyEngaged")
            baware.setTrackingMode("Head")  
            baware.setStimulusDetectionEnabled("Sound", True)
            baware.setStimulusDetectionEnabled("Movement", True)
            baware.setStimulusDetectionEnabled("People", True)
            baware.setStimulusDetectionEnabled("Touch", False)
        else:
            self.logger.debug("Not setting up Basic Awareness")

    def setupASR(self):
        if self.hasHandle("ALSpeechRecognition"):
            asr = self.handles["ALSpeechRecognition"]
            asr.setVisualExpression(False)
            asr.setAudioExpression(False)
        else:
            self.logger.debug("Not setting up Speech Recognition")

    # -------------------------------------
    # Callbacks
    # -------------------------------------

    def blinkingCallback(self, event_name, blink_frequency):
        """ Make Nao Blink in whatever color was set"""
        
        self.blink_frequency = blink_frequency
        self.handles["leds"].blink(0.2)
        random_delay = random.random() * blink_frequency / 2.0
        time.sleep((random_delay + blink_frequency) / 1000.0)
        
        if self.is_blinking:
        	self.handles["ALMemory"].raiseEvent("emoBlink", blink_frequency)
            

    def WordRecognizedCallback(self, eventName, value):
        """ If a word was recognized either shine green (understood)
            or flash red (not understood)"""
        self.handles["ALMemory"].unsubscribeToEvent("WordRecognized", self.name)
        
        self.logger.debug("Word Recognized Triggered with confidence %s", value[1])

        if float(value[1]) > 0.5:
            self.handles["leds"].set_eyes('g')
            self.handles["leds"].eyes_on()
            self.logger.debug("I have understood.")
        elif float(value[1]) > 0.20:
            self.handles["leds"].set_eyes('r')
            self.handles["leds"].eyes_on()
                
            self.logger.debug("Eyes Have flashed.")

        time.sleep(0.5)
        self.handles["leds"].set_eyes('w')
        self.handles["leds"].eyes_on()
        

        
        self.handles["ALMemory"].subscribeToEvent("WordRecognized", self.name, "WordRecognizedCallback")

    def SpeechStatusCallback(self, eventName, status):
        """ Report speech through ears only """

        if status == "Idle":
            pass
        elif status == "ListenOn":
            pass
        elif status == "SpeechDetected":
            self.handles["leds"].ears_on()
        elif status == "EndOfProcess":
            self.handles["leds"].ears_off()
        elif status == "ListenOff":
            pass
        elif status == "Stop":
            pass

    # -------------------------------------
    # Overwritten from NaoModule
    # -------------------------------------

    def __enter__(self):
        if self.hasAllHandles(["ALBasicAwareness", "ALMotion"]):
            self.handles["ALMotion"].wakeUp()
            self.handles["ALBasicAwareness"].startAwareness()

        return self

    def __exit__(self, exec_type, exec_value, traceback):
    	self.is_blinking = False
    	time.sleep(1)
    	self.handles["leds"].eyes_on()
        if self.hasAllHandles(["ALBasicAwareness", "ALMotion"]):
            self.handles["ALBasicAwareness"].stopAwareness()
            self.handles["ALMotion"].rest()
