import random
from naoqi import ALProxy
from naoqi import ALModule
import os
import logging

from Question import Question
from Animal import Animal
import utility as util


class GameModule(ALModule):
    def __init__(self, name, on_robot):
        ALModule.__init__(self, name)
        self.name = name

        logging.basicConfig()
        self.logger = logging.getLogger(__name__)
        self.logger.info("Logging enabled for: " + self.name)

        # get all the proxies used by this module
        self.tts = ALProxy("mood")
        self.memory = ALProxy("ALMemory")
        self.dialog = ALProxy("ALDialog")
        self.speech = ALProxy("speech_module")
        self.params = ALProxy("parameter_server")

        # pesky base path again -- should refactor this
        base_dir = os.path.dirname(__file__)
        base_dir = os.path.join(base_dir, "..", "..")
        self.base_dir = os.path.abspath(base_dir)
        self.logger.debug("Base path:" + self.base_dir)
          
        # initialize class attributes
        self.text = ""
        self.is_guess = False
        self.current_question_wrapper = dict()
        self.asked_questions = list()
        self.active_questions = list()
        self.active_animals = list()
        self.registered_topics = list()
        self.num_asked = 0
        self.game_in_progress = False

        # load question topics
        question_list = self.params.getParameter(self.name, 'questions')
        for rel_path in question_list:
            self.logger.debug("Trying to load path: %s" % rel_path)
            abs_path = util.getAbsPath(self.base_dir , rel_path)
            question = Question(abs_path)

            if on_robot:
                topic_path = util.getAbsPath("/home/nao/naoProject", question.topic)
            else:
                topic_path = util.getAbsPath(self.base_dir , question.topic)
            name = self.dialog.loadTopic(topic_path)
            self.registered_topics.append(name)

        # load guess question    
        guess_path_relative = self.params.getParameter(self.name,"guess")
        abs_path = util.getAbsPath(self.base_dir , guess_path_relative)
        self.guess_question = Question(abs_path)

        # load guess' topic
        if on_robot:
            abs_path = util.getAbsPath("/home/nao/naoProject", self.guess_question.topic)
        else:
            abs_path = util.getAbsPath(self.base_dir , self.guess_question.topic)
        name = self.dialog.loadTopic(abs_path)
        self.registered_topics.append(name)

        # register menu callbacks
        self.memory.subscribeToEvent("NewGame", self.name, "NewGameCallback")
        self.dialog.subscribe(self.name)

        # register menu topic (aka activate the game)
        rel_path = self.params.getParameter(self.name, "menu")
        if on_robot:
            abs_path = util.getAbsPath("/home/nao/naoProject", rel_path)
        else:
            abs_path = util.getAbsPath(base_dir , rel_path)
        self.speech.addMenuTopic(abs_path)

    def __enter__(self):
        return self

    def __exit__(self, exec_type, exec_value, traceback):
        # unload question topics
        self.dialog.unsubscribe(self.name)
        for topic in self.registered_topics:
            self.dialog.unloadTopic(topic)
        return

    def NewGameCallback(self, eventName, value):
        self.logger.info("Setting up a new game.")

        if self.game_in_progress:
            system.info("Overwriting a game in progress.")
        
        # load questions
        self.active_questions = list()
        question_list = self.params.getParameter(self.name,'questions')
        for rel_path in question_list:
            abs_path = util.getAbsPath(self.base_dir , rel_path)
            question = Question(abs_path)
            self.active_questions.append(question)

        # load animals
        self.animal_list = list()
        animal_list = self.params.getParameter(self.name,"animals")
        for animal_path in animal_list:
            abs_path = util.getAbsPath(self.base_dir , animal_path)
            animal = Animal(abs_path, self.active_questions)
            self.active_animals.append(animal)

        # reset the number of questions asked
        self.num_asked = 0
        self.game_in_progress = True

        # allow next move to start a new game
        self.memory.subscribeToEvent("nextMove", self.name, "nextMoveCallback")

    def nextMoveCallback(self, eventName, value):
        self.memory.unsubscribeToEvent("nextMove", self.name)

        self.logger.debug("Active Questions: " + str(len(self.active_questions)))
        self.logger.debug("Active Animals: " + str(len(self.active_animals)))

        if (len(self.active_animals) <= 0):
            self.tts.say("I concede, I don't know the animal.")
            self.tts.say("If you want to play again, say new game")
            self.game_in_progress = False
            return

        # choose between question or guess
        if len(self.active_questions) <= 0:
            self.prepareGuess()
            self.is_guess = True
        elif random.random() > 0.2:
            self.prepareQuestion()
            self.is_guess = False
            self.logger.debug("The relative distribution over answers: ")
            for animal in self.active_animals:
                self.logger.debug(animal.answers[self.question.qid].relativeLabelPropability)
        else:
            print("Random guess")
            self.prepareGuess()
            self.is_guess = True

        self.tts.say(self.text)
        self.question.activate()
        self.dialog.activateTopic(self.question.topic_name)

    def AskedQuestionCallback(self, label, value):
        self.logger.debug("AskedQuestionCallback executed")
        self.question.deactivate()
        self.dialog.deactivateTopic(self.question.topic_name)

        game_event = list()
        game_event.append(self.text)
        game_event.append(label)
        self.memory.raiseEvent("GameEvent", game_event)

        # if question update animals based on label
        if not self.is_guess:
            self.current_question_wrapper["label"] = label
            self.asked_questions.append(self.current_question_wrapper)
            self.current_question_wrapper = dict()
            for animal in self.active_animals:
                answer = animal.answers[self.question.qid] 
                animal.propability *= answer.relativeLabelPropability[label]
                
        self.normalizeAnimalPropability()
        self.removeUnlikelyAnimals()
        self.num_asked += 1

        # if guess check if correct
        if self.is_guess and label == "yes":
            self.tts.say("I win! You thought of " + self.animal.name)
            self.active_animals = dict()
            self.game_in_progress = False
            self.logger.info("Question Traceback: ")
            for question_wrapper in self.asked_questions:
                self.logger.info(str(question_wrapper["QID"]) + " with answer: " + question_wrapper["label"])
            return

        # if maximum amount of questions asked loose
        if self.params.getParameter(self.name,"max_questions") <= self.num_asked:
            self.tts.say("Okay, I don't know the animal. You Win!")
            self.game_in_progress = False
            return

        self.memory.subscribeToEvent("nextMove",self.name, "nextMoveCallback")

    def normalizeAnimalPropability(self):
        propability_sum = 0.0
        for animal in self.active_animals:
            propability_sum += animal.propability

        for animal in self.active_animals:
            animal.propability /= propability_sum

    def removeUnlikelyAnimals(self):
        new_active_animals = list()
        for animal in self.active_animals:
            if animal.propability <= self.params.getParameter(self.name,"discard_propability"):
                self.logger.debug( "Low propability (%d), discarding: %s" %\
                                   (animal.propability, animal.name))
            else:
                new_active_animals.append(animal)

        self.active_animals = new_active_animals

    def prepareQuestion(self):
        best_question = self.active_questions[0]
        for question in self.active_questions:
            question.updateScore(self.active_animals)
            if question.score > best_question.score:
                best_question = question

        self.question = best_question
        self.active_questions.remove(self.question)
        self.current_question_wrapper["QID"] = self.question.qid
        
        self.text = self.question.text 
        self.logger.debug("Asking: " + best_question.text)

        # generate answer distribution for question
        answer_distribution_sum = dict()
        for label in self.question.labels:
            answer_distribution_sum[label] = 0.0
        
        for animal in self.active_animals:
            dist = animal.getAnswerDistribution(self.question.qid)
            for label in dist:
                answer_distribution_sum[label] += dist[label] 
                        
        for animal in self.active_animals:
            answer = animal.answers[self.question.qid]
            answer.setRelativePropability(answer_distribution_sum)

    def prepareGuess(self):
        self.question = self.guess_question
        
        best_animal = self.active_animals[0]
        for animal in self.active_animals:
            if animal.propability > best_animal.propability:
                best_animal = animal
        self.animal = best_animal
        self.active_animals.remove(best_animal)
        
        self.text = best_animal.text
        self.logger.debug("Asking: " + best_animal.text)

