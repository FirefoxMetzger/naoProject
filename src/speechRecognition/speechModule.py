import sys

from naoqi import ALModule
from naoqi import ALProxy

class SpeechModule(ALModule):
    def __init__(self, name):
        ALModule.__init__(self, name)
        self.name = name

        self.memory = ALProxy("ALMemory")
        self.tts = ALProxy("ALTextToSpeech")
        self.touch = ALProxy("ALTouch")
    
        self.dialog = ALProxy("ALDialog")
        self.dialog.setLanguage("English")

        self.menu_topics = list()
        self.module_topics = list()

        self.memory.subscribeToEvent("HandRightBackTouched",self.name,"touchCallback")
        self.dialog.subscribe(self.name)

    def __enter__(self):
        return self

    def __exit__(self, exec_type, exec_value, traceback):
        self.dialog.unsubscribe(self.name)
        for topic in self.menu_topics:
            self.dialog.unloadTopic(topic)

    def speechCallback(self, eventName, value, subscriberIdentifier):
        """ Comment needed to bind method

        """
        pass

    def touchCallback(self, eventName, val, subscriberIdentifier):
        """ Commend needed

        """
        if val == 0.0:
            return

        self.memory.unsubscribeToEvent("HandRightBackTouched",self.name)
        print("Stopped speach") 
        self.tts.stopAll()
        self.memory.subscribeToEvent("HandRightBackTouched",self.name,"touchCallback")

    def addMenuTopic(self, topic_path):
        """


        """
        try:
            name = self.dialog.loadTopic(topic_path)
        except RuntimeError:
            print("Topic already loaded.")
        else:
            self.menu_topics.append(name)
            self.activateMenu()

    def removeMenuTopic(self, name):
        """

        """
        try:
            self.menu_topics.remove(name)
        except ValueError:
            print("Topic name unknown")
        else:
            self.dialog.unloadTopic(name)

    def activateMenu(self):
        for topic_name in self.menu_topics:
            self.dialog.activateTopic(topic_name)

    def deactivateMenu(self):
        for topic in self.menu_topics:
            topic_name = topic["name"]
            self.dialog.deactivateTopic(topic_name)
