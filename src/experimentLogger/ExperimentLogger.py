import logging
import time
import os
import random
import yaml
import string
from naoqi import ALProxy
from naoqi import ALModule

class ExperimentLogger(ALModule):
    def __init__(self, name):
        ALModule.__init__(self, name)
        self.name = name

        logging.basicConfig()
        self.logger = logging.getLogger(__name__)
        self.logger.info("Logging enabled for: " + self.name)

        self.memory = ALProxy("ALMemory")
        try:
            self.speechRec = ALProxy("ALSpeechRecognition")
        except RuntimeError:
            self.has_speechDetection = False
            self.logger.warning("Speech detection unaviable.")
            self.memory.declareEvent("WordRecognized")
        else:
            self.has_speechDetection = True
            self.logger.info("Speech detection engine found.")
            
        self.memory.subscribeToEvent("WordRecognized", self.name,\
                                  "WordRecognizedCallback")

        self.memory.declareEvent("NewGame")
        self.memory.subscribeToEvent("NewGame", self.name,\
                                     "NewGameCallback")
        self.logger.debug("Logger subscribed.")

        base_path = os.path.dirname(__file__)
        base_path = os.path.join(base_path, "..", "..")
        self.base_path = os.path.abspath(base_path)

        self.current_user = self.generateName()
        self.previous_games = 0
        self.game_running = False

        #user data        
        self.experiment_data = dict()
        self.experiment_data["user"] = self.current_user
        self.experiment_data["previous_games"] = 0
        self.experiment_data["recognized"] = list()

    def __enter__(self):
        return self

    def __exit__(self, exec_type, exec_value, traceback):
        self.memory.unsubscribeToEvent("WordRecognized",self.name)
        return

    def WordRecognizedCallback(self, eventName, value):
        detection = dict()
        detection["word"] = value[0]
        detection["confidence"] = value[1]
        detection["timestamp"] = time.time()

        self.experiment_data["recognized"].append(detection)
        self.logger.debug("Detected: %s" % value)
        return

    def NewGameCallback(self, eventName, is_new_user):
        #save old log
        path = ["experimentData"]
        abs_path = self.getAbsPath(path)

        if self.previous_games == 0:
            file_name = self.current_user
        else:
            file_name = self.current_user + ('_'+str(self.previous_games))
        file_name = file_name + ('.log')
        
        file_path = os.path.join(abs_path,file_name)

        with open(file_path, 'w') as output:
            yaml.dump(self.experiment_data, output, default_flow_style=False)
            self.logger.info("Saved experiment to: %s" % abs_path)

        #setup new log with increased counter
        if is_new_user == 1:
            self.current_user = self.generateName()
            self.previous_games = 0
        else:
            self.previous_games += 1
            
        self.experiment_data = dict()
        self.experiment_data["user"] = self.current_user
        self.experiment_data["previous_games"] = self.previous_games
        self.experiment_data["recognized"] = list()

    def generateName(self):
        path = ["experimentData"]
        data_folder = self.getAbsPath(path)
        used_names = os.listdir(data_folder)

        base = string.letters + string.digits
        length = 7 
        def randomName():
            characters = [random.choice(base) for _ in range(0,length)]
            name = ''.join(characters)
            return name

        name = randomName()
        while name.join('.log') in used_names:
            name = randomName()

        return name

    def getAbsPath(self,rel_path):
        path = self.base_path
        for chunk in rel_path:
            path = os.path.join(path, chunk)

        return os.path.abspath(path)
