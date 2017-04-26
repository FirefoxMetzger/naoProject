import random
from naoqi import ALProxy
from naoqi import ALModule
import os
import logging

from Question import Question
from Animal import Animal
import utility as util

class GameModule(ALModule):
    def __init__(self, name):
        ALModule.__init__(self, name)
        self.name = name

        logging.basicConfig()
        self.logger = logging.getLogger(__name__)
        self.logger.info("Logging enabled for: " + self.name)

        # init text to speach proxy
        self.tts = ALProxy("ALTextToSpeech")
        self.memory = ALProxy("ALMemory")
        self.dialog = ALProxy("ALDialog")
        self.speech = ALProxy("speech_module")
        self.params = ALProxy("parameter_server")

        modules = self.params.getModuleList()
        if self.name in modules:
            self.logger.debug("Found my configuration parameters.")

        self.registered_topics = list()
        self.active_questions = list()
        self.active_animals = list()

        base_dir = os.path.dirname(__file__)
        base_dir = os.path.join(base_dir, "..", "..")
        self.base_dir = os.path.abspath(base_dir)
        self.logger.debug("Base path:" + self.base_dir)

        # load questions
        question_list = self.params.getParameter(self.name,'questions')
        for rel_path in question_list:
            abs_path = util.getAbsPath(self.base_dir , rel_path)
            question = Question(abs_path)
            self.active_questions.append(question)
            
            question_path = util.getAbsPath(self.base_dir , question.topic)
            name = self.dialog.loadTopic(question_path)
            self.registered_topics.append(name)
            
        guess_path_relative = self.params.getParameter(self.name,"guess")
        abs_path = util.getAbsPath(base_dir , guess_path_relative)
        self.guess_question = Question(abs_path)
        
        abs_path = util.getAbsPath(base_dir , self.guess_question.topic)
        name = self.dialog.loadTopic(abs_path)
        self.registered_topics.append(name)

        # load animals
        animal_list = self.params.getParameter(self.name,"animals")
        for animal_path in animal_list:
            abs_path = util.getAbsPath(base_dir , animal_path)
            animal = Animal(abs_path, self.active_questions)
            self.active_animals.append(animal)
        
        self.text = ""
        self.is_guess = False

        self.current_question_wrapper = dict()
        self.asked_questions = list()

        self.dialog.subscribe(self.name)
        self.num_asked = 0

        rel_path = self.params.getParameter(self.name, "menu")
        abs_path = util.getAbsPath(base_dir , rel_path)
        self.speech.addMenuTopic(abs_path)
        self.memory.subscribeToEvent("nextMove", self.name, "nextMoveCallback")

    def __enter__(self):
        return self

    def __exit__(self, exec_type, exec_value, traceback):
        self.dialog.unsubscribe(self.name)
        for topic in self.registered_topics:
            self.dialog.unloadTopic(topic)
        return

    def nextMoveCallback(self, eventName, value):
        self.memory.unsubscribeToEvent("nextMove", self.name)
        self.gameTurn()

    def gameTurn(self):
        self.logger.debug("Active Questions: " + str(len(self.active_questions)))
        self.logger.debug("Active Animals: " + str(len(self.active_animals)))

        if (len(self.active_animals) <= 0):
            self.tts.say("I don't have any more animals to guess.")
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

        # if guess check if correct
        if self.is_guess and label == "yes":
            self.tts.say("I have won. You thought of " + self.animal.name)
            self.active_animals = dict()
            self.logger.info("Question Traceback: ")
            for question_wrapper in self.asked_questions:
                self.logger.info(str(question_wrapper["QID"]) + " with answer: " + question_wrapper["label"] )

        # if maximum amount of questions asked loose
        self.num_asked += 1
        if self.params.getParameter(self.name,"max_questions") <= self.num_asked:
            self.tts.say("Okay, I don't know the animal. Please tell me.")

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

