import logging
import fractions
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
            baware.setEngagementMode("SemiEngaged")
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

    def blinkingCallback(self, event_name, update_frequency):
        """ Make Nao Blink in whatever color was set"""
        update_frequency = int(update_frequency)
        counter = 0
        cycle_time = fractions.gcd(update_frequency, self.blink_frequency)
        while self.is_blinking:
            if (counter * cycle_time) % update_frequency == 0:
                cycle_time = fractions.gcd(update_frequency,\
                    self.blink_frequency)
                counter = 0

            if (counter * cycle_time) % self.blink_frequency == 0:
                self.getHandle("leds").blink(0.6)

            time.sleep(cycle_time)
            counter += 1

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
            self.getHandle("ALMotion").wakeUp()
            self.basic_awareness.startAwareness()

        if self.hasAllHandles(["ALMemory" "leds"]):
            self.getHandle("ALMemory").raiseEvent("emoBlink", 250)
        return self

    def __exit__(self, exec_type, exec_value, traceback):
        if self.hasAllHandles(["ALBasicAwareness", "ALMotion"]):
            self.basic_awareness.stopAwareness()
            self.motion.sleep()
