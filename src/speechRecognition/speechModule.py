import sys
import logging

from naoqi import ALModule
from naoqi import ALProxy

class SpeechModule(ALModule):
    def __init__(self, name):
        ALModule.__init__(self, name)
        self.name = name

        logging.basicConfig()
        self.logger = logging.getLogger(__name__)
        self.logger.info("Logging enabled for: " + self.name)

        self.memory = ALProxy("ALMemory")
        self.tts = ALProxy("ALTextToSpeech")
        self.touch = ALProxy("ALTouch")
    
        self.dialog = ALProxy("ALDialog")
        self.dialog.setLanguage("English")

        self.menu_topics = list()

        self.memory.subscribeToEvent("HandRightBackTouched",self.name,"touchCallback")
        self.dialog.subscribe(self.name)
   
    def __enter__(self):
        return self

    def __exit__(self, exec_type, exec_value, traceback):
        self.dialog.unsubscribe(self.name)
        for topic in self.menu_topics:
            self.dialog.unloadTopic(topic)

    def addMenuTopic(self, topic_path):
        try:
            name = self.dialog.loadTopic(topic_path)
        except RuntimeError:
            self.logger.warning("Topic already loaded. From: %s" %\
                                (topic_path))
        else:
            self.menu_topics.append(name)
            self.logger.debug("Added topic %s" % (name))
            self.activateMenu()

    def activateMenu(self):
        for topic_name in self.menu_topics:
            self.dialog.activateTopic(topic_name)

    def deactivateMenu(self):
        for topic in self.menu_topics:
            topic_name = topic["name"]
            self.dialog.deactivateTopic(topic_name)
