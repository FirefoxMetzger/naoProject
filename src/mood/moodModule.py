import logging
import fractions
import time

from naoqi import ALModule
from naoqi import ALProxy

class MoodModule(ALModule):
    def __init__(self, name):
        ALModule.__init__(self, name)
        self.name = name

        logging.basicConfig()
        self.logger = logging.getLogger(__name__)
        self.logger.info("Logging enabled for: " + self.name)

        self.handles = dict()
        
        self.setupMemory()
        self.getHandle("ALMotion")
        self.getHandle("leds")
        self.setupASR()
        self.setupBasicAwareness()
        
        self.blink_frequency = 500 #ms
        self.is_blinking = True

    def __enter__(self):
        if self.hasAllHandles(["ALBasicAwareness", "ALMotion"]):
            self.getHandle("ALMotion").wakeUp()
            self.basic_awareness.startAwareness()

        if self.hasAllHandles(["ALMemory" "leds"]):
            self.memory.raiseEvent("emoBlink", 250)
        return self

    def __exit__(self, exec_type, exec_value, traceback):
        if self.hasHandles(["ALBasicAwareness", "ALMotion"]):
            self.basic_awareness.stopAwareness()
            self.motion.sleep()

    def setupMemory(self):
        self.getHandle("ALMemory", True)
        if self.hasHandle("ALMemory"):
            memory = self.handles["ALMemory"]
            memory.subscribeToEvent("emoBlink", self.name, "blinkingCallback")
            memory.subscribeToEvent("ALSpeechRecognition/Status", self.name,\
                                     "SpeechStatusCallback")
            memory.subscribeToEvent("WordRecognized", self.name, "WordRecognized")
        else:
            self.logger.debug("Not setting up any callbacks")

    def setupBasicAwareness(self):
        self.getHandle("ALBasicAwareness")
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
        self.getHandle("ALSpeechRecognition")
        if self.hasHandle("ALSpeechRecognition"):
            asr = self.handles["ALSpeechRecognition"]
            asr.setVisualExpression(False)
            asr.setAudioExpression(False)
        else:
            self.logger.info("Not setting up Speech Recognition")

    def hasAllHandles(self, module_names):
        has_all = True
        for module in module_names:
            has_all = ( has_all and self.hasHandle(module) )

    def hasHandle(self, module_name):
        if module_name in self.handles.keys():
            return True
        else:
            return False

    def getHandle(self, module_name, is_critical=False):
        self.logger.debug("Getting module %s" % module_name)

        try:
            handle = ALProxy(module_name)
        except RuntimeError:
            if is_critical:
                self.logger.critical("Could not load module %s" % module_name)
            else:
                self.logger.warning("Could not load module %s" % module_name)
        else:
            self.handles[module_name] = handle
            self.logger.debug("Added handle to %s" % module_name)

    def blinkingCallback(self, event_name, update_frequency):
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
        self.memory.unsubscribeToEvent("WordRecognized", self.name)

        if value[2] > 0.5:
            self.leds.set_eyes('g')
            self.leds.eyes_on()
        elif value[2] > 0.35:
            self.leds.set_eyes('r')
            for idx in range(0,5):
                self.leds.eyes_on()
                time.sleep(0.05)
                self.leds.eyes_off()

        time.sleep(0.5)
        self.leds.set_eyes('w')
        self.leds.eyes_on()
        
        self.memory.subscribeToEvent("WordRecognized", self.name, "WordRecognized")

    def SpeechStatusCallback(self, eventName, status):
        self.memory.unsubscribeToEvent("ALSpeechRecognition/Status", self.name)

        if status == "Idle":
            pass
        elif status == "ListenOn":
            pass
        elif status == "SpeechDetected":
            self.leds.ears_on()
        elif status == "EndOfProcess":
            self.leds.ears_off()
        elif status == "ListenOff":
            pass
        elif status == "Stop":
            pass
        
        self.memory.subscribeToEvent("ALSpeechRecognition/Status", self.name,\
                                     "SpeechStatusCallback")
