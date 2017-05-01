import random
import os
import time

from NaoModule import NaoModule
from core.Question import Question
from core.Animal import Animal

class GameModule(NaoModule):

    # -------------------------------------
    # Setup Module
    # -------------------------------------
    
    def __init__(self, name, on_robot):
        NaoModule.__init__(self, name)
        self.on_robot = on_robot

        # get all the proxies used by this module
        self.getHandle("mood")
        self.getHandle("ALMemory", True)
        self.getHandle("ALDialog")
        self.getHandle("speech_module")
        self.getHandle("parameter_server", True)
        self.getHandle("ALTextToSpeech")
          
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

        # setup Proxy stuff
        self.setupALDialog()
        

    def setupALDialog(self):
        # load question topics
        question_list = self.handles["parameter_server"].getParameter(self.name, 'questions')
        for rel_path in question_list:
            abs_path = self.getAbsPath(rel_path)
            question = Question(abs_path)
            self.loadQiChatTopic(question.topic)

        # load guess question    
        guess_rel_dir = self.handles["parameter_server"].getParameter(self.name, "guess")
        abs_path = self.getAbsPath(guess_rel_dir)
        self.guess_question = Question(abs_path)
        self.loadQiChatTopic(self.guess_question.topic)

        # register menu topic (aka activate the game)
        rel_path = self.handles["parameter_server"].getParameter(self.name, "menu")
        abs_path = self.getTopicAbsPath(rel_path)
        self.handles["speech_module"].addMenuTopic(abs_path)
        
        self.handles["ALDialog"].compileAll()

    def getTopicAbsPath(self, rel_path):
        if self.on_robot:
            abs_path = self.getAbsPath(rel_path, "/home/nao/naoProject")   
        else:
            abs_path = self.getAbsPath(rel_path)

        return abs_path

    def loadQiChatTopic(self, rel_path):
        abs_path = self.getTopicAbsPath(rel_path)
        self.logger.debug("Loading QiChat topic from %s" % abs_path)

        if self.hasHandle("ALDialog"):
            name = self.handles["ALDialog"].loadTopic(abs_path)
            self.registered_topics.append(name)
        else:
            self.logger.debug("No ALDialog. Not loading topic.")

    # -------------------------------------
    # Callbacks
    # -------------------------------------

    def NewGameCallback(self, eventName, value):
        """ Reset the Game """
        self.logger.info("Setting up a new game.")

        if self.game_in_progress:
            self.logger.info("Overwriting a game in progress.")
        
        # load questions
        self.active_questions = list()
        question_list = self.handles["parameter_server"].getParameter(self.name,'questions')
        for rel_path in question_list:
            abs_path = self.getAbsPath(rel_path)
            question = Question(abs_path)
            self.active_questions.append(question)

        # load animals
        self.active_animals = list()
        animal_list = self.handles["parameter_server"].getParameter(self.name, "animals")
        for animal_path in animal_list:
            abs_path = self.getAbsPath(animal_path)
            animal = Animal(abs_path, self.active_questions)
            self.active_animals.append(animal)

        # reset the number of questions asked
        self.num_asked = 0
        self.game_in_progress = True

        # allow next move to start a new game
        self.handles["ALMemory"].subscribeToEvent("nextMove", self.name, "nextMoveCallback")

    def nextMoveCallback(self, eventName, value):
        """ Prepare the next move (question or guess) """
        self.handles["ALMemory"].unsubscribeToEvent("nextMove", self.name)

        self.logger.debug("Active Questions: " + str(len(self.active_questions)))
        self.logger.debug("Active Animals: " + str(len(self.active_animals)))

        if (len(self.active_animals) <= 0):
            self.handles["ALTextToSpeech"].say("I concede, I don't know the animal.")
            self.handles["ALTextToSpeech"].say("If you want to play again, say new game")
            self.handles["ALMemory"].raiseEvent("EndGame", 0)
            self.game_in_progress = False
            return

        # choose between question or guess
        if len(self.active_questions) <= 0:
            self.prepareGuess()
            self.is_guess = True
        elif self.isAskQuestion():
            self.prepareQuestion()
            self.is_guess = False
        else:
            self.prepareGuess()
            self.is_guess = True

        self.handles["ALDialog"].activateTopic(self.question.topic_name)
        self.question.activate()
        self.handles["ALMemory"].raiseEvent("QuestionAsked", self.question.qid)  

    def AskedQuestionCallback(self, label, value):
        """ A question has been answered. Update propabilities """
        self.question.deactivate()
        self.handles["ALDialog"].deactivateTopic(self.question.topic_name)

        game_event = list()
        game_event.append(self.text)
        game_event.append(label)
        self.handles["ALMemory"].raiseEvent("GameEvent", game_event)

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
            self.handles["ALTextToSpeech"].say("I win! You thought of " + self.animal.name)
            self.handles["ALMemory"].raiseEvent("EndGame", 1)
            self.active_animals = dict()
            self.game_in_progress = False
            self.logger.info("Question Traceback: ")
            for question_wrapper in self.asked_questions:
                self.logger.info(str(question_wrapper["QID"]) + " with answer: " + question_wrapper["label"])
            return

        # if maximum amount of questions asked loose
        if self.handles["parameter_server"].getParameter(self.name,"max_questions") <= self.num_asked:
            self.handles["ALTextToSpeech"].say("Okay, I don't know the animal. You Win!")
            self.handles["ALMemory"].raiseEvent("EndGame", 0)
            self.game_in_progress = False
            return

        self.handles["ALMemory"].subscribeToEvent("nextMove",self.name, "nextMoveCallback")
        time.sleep(0.7)
        if self.game_in_progress:
            self.handles["ALMemory"].raiseEvent("NextMoveSayText",1)
        
    def QuestionAskedCallback(self, eventName, value):
        """ Say the guess question """
        if value != "guess":
            return
        self.handles["ALTextToSpeech"].say(self.text)

    # -------------------------------------
    # Overwritten from NaoModule
    # -------------------------------------

    def __enter__(self):
        if self.hasHandle("ALMemory"):
            memory = self.handles["ALMemory"]
            memory.subscribeToEvent("NewGame", self.name, "NewGameCallback")
            memory.subscribeToEvent("QuestionAsked", self.name, "QuestionAskedCallback")
        else:
            self.logger.debug("No Handle to ALMemory")

        if self.hasHandle("ALDialog"):
            dialog = self.handles["ALDialog"]
            dialog.subscribe(self.name)
            
            speech = self.handles["speech_module"]
            speech.deactivateMenu()
            speech.activateMenu()
        else:
            self.logger.debug("No Handle to ALMemory")
        
        return self

    def __exit__(self, exec_type, exec_value, traceback):
        if self.hasHandle("ALMemory"):
            memory = self.handles["ALMemory"]
            memory.unsubscribeToEvent("NewGame", self.name)
        else:
            self.logger.debug("No Handle to ALMemory")
        
        if self.hasHandle("ALDialog"):
            dialog = self.handles["ALDialog"]
            dialog.unsubscribe(self.name)
            for topic in self.registered_topics:
                dialog.unloadTopic(topic)
        else:
            self.logger.debug("No Handle to ALMemory")

        return
        
    # -------------------------------------
    # Private methods
    # -------------------------------------

    def normalizeAnimalPropability(self):
        propability_sum = 0.0
        for animal in self.active_animals:
            propability_sum += animal.propability

        for animal in self.active_animals:
            animal.propability /= propability_sum
            animal.propability *= len(self.active_animals)

    def removeUnlikelyAnimals(self):
        new_active_animals = list()
        for animal in self.active_animals:
            if animal.propability <= self.handles["parameter_server"].getParameter(self.name,"discard_propability"):
                self.logger.debug( "Low propability (%d), discarding: %s" %\
                                   (animal.propability, animal.name))
            else:
                new_active_animals.append(animal)

        self.active_animals = new_active_animals

    def prepareQuestion(self):
    
        self.question = self.pickBestQuestion()
        self.active_questions.remove(self.question)
        self.current_question_wrapper["QID"] = self.question.qid
        
        self.text = self.question.text 
        self.logger.debug("Asking: " + self.question.text)

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
        
    def pickBestQuestion(self):
        best_question = self.active_questions[0]
        for question in self.active_questions:
            question.updateScore(self.active_animals)
            if question.score > best_question.score:
                best_question = question
        return best_question

    def isAskQuestion(self):
        #return True if we ask a quesstion, False otherwise
        num_animals = len(self.active_animals)
        remaining_questions = self.handles["parameter_server"].getParameter(self.name,"max_questions") - self.num_asked
        if num_animals < 3:
            return False
        elif remaining_questions <= self.handles["parameter_server"].getParameter(self.name,"panic_questions"):
            return False
        return True

