import logging
import time
import os
import random
import yaml
import string

from NaoModule import NaoModule

class ExperimentLogger(NaoModule):
    def __init__(self, name):
        NaoModule.__init__(self, name)

        self.getHandle("ALMemory")

        self.current_user = self.generateName()
        self.previous_games = 0
        self.game_running = False

        #user data
        self.experiment_data = dict()
        self.resetExperiment()

        if self.hasHandle("ALMemory"):
            self.handles["ALMemory"].subscribeToEvent("WordRecognized", self.name,\
                    "WordRecognizedCallback")
            self.handles["ALMemory"].subscribeToEvent("GameEvent", self.name, \
                    "GameEventCallback")
            self.handles["ALMemory"].subscribeToEvent("NewGame", self.name,\
                    "NewGameCallback")
            self.logger.debug("Logger subscribed.")
        else:
            self.logger.error("Unable to subscribe to Events. Experiment logging disabled.")

    def __exit__(self, exec_type, exec_value, traceback):
        if self.hasHandle("ALMemory"):
            self.handles["ALMemory"].unsubscribeToEvent(\
                "WordRecognized",self.name)
            self.handles["ALMemory"].unsubscribeToEvent(\
                "GameEvent",self.name)
            self.handles["ALMemory"].unsubscribeToEvent(\
                "NewGame",self.name)
        return

    def GameEventCallback(self, eventName, value):
        """Add a new question / answer pair to the log"""
        
        self.logger.debug("Saving another game event.")
        game_event = dict()
        game_event["question"] = value[0]
        game_event["answer"] = value[1]
        game_event["timestamp"] = time.time()

        self.experiment_data["game_event"].append(game_event)

    def WordRecognizedCallback(self, eventName, value):
        """Add a new word to the log"""
        
        detection = dict()
        detection["word"] = value[0]
        detection["confidence"] = value[1]
        detection["timestamp"] = time.time()

        self.experiment_data["recognized"].append(detection)
        self.logger.debug("Detected: %s" % value)

    def NewGameCallback(self, eventName, is_new_user):
        """Start a new log"""
        
        self.logger.debug("Saving new game Event.")
        
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
            self.logger.info("New user with name: %s" % self.current_user)
            self.previous_games = 0
        else:
            self.previous_games += 1

        self.resetExperiment()
        
    def resetExperiment(self):
        self.experiment_data = dict()
        self.experiment_data["user"] = self.current_user
        self.experiment_data["previous_games"] = self.previous_games
        self.experiment_data["recognized"] = list()
        self.experiment_data["game_event"] = list()

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
