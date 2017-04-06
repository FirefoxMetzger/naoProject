import ConfigParser
import copy
import os
import json

from naoqi import ALProxy

from Question import Question
from Animal import Animal

class Game:
    def __init__(self,config,tts):

        self.tts = tts
        
        #load the database
        self.animal_path = config.get("GameFabric","animal_path")
        self.question_path = config.get("GameFabric","question_path")

        self.questions = self.buildQuestionsFromDatabase()
        qid_list = list()
        for question in self.questions:
            try:
                assert not question.qid in qid_list
            except (AssertionError):
                raise ValueError(
                    "The QIDs are not unique! Tested: " +
                    str(question.qid))
            else:
                qid_list.append(question.qid)
                
        self.animals = self.buildAnimalsFromDatabase()
        self.normalizeAnimalPropability()
        
        #set some "environment variables"
        self.is_won = False # true if Nao guessed the animal
        self.number_of_questions = config.getint("Game","max_questions")
        self.num_asked = -1
        self.panic_threshold = config.getint("Game","panic_questions")
        self.confidence_for_certain = config.getfloat(
                "Game",
                "confidence_for_certain")
        self.confidence_for_discard = config.getfloat("Game","confidence_for_discard")
		
    def loop(self):
        if self.is_won:
            say_string = ("The game is already over. You thought about " + 
            self.animals[0].name)
            print(say_string)
            self.tts.say(str(say_string))
            return

        if self.num_asked == -1:
            say_string = "Okay. Think of an animal.. When you are ready touch my head."
            print(say_string)
            self.tts.say(str(say_string))
            
        else:
            for animal in self.animals:
                if animal.propability >= self.confidence_for_certain:
                    self.askSpecificQuestion(animal)
                    break
            else:
                if self.num_asked < self.number_of_questions - self.panic_threshold:
                    # Try to find the animal
                    self.askDifferentiatingQuestion()
                else:
                    # Panic mode, just try best guesses
                    animal = self.getBestAnimal()
                    self.askSpecificQuestion(animal)
        self.num_asked += 1
		
    def askSpecificQuestion(self, animal):
        question_string = "Is it a " + animal.name + "?"
        print(str(question_string))
        self.tts.say(str(question_string))

        answer = "Yes"
        #TODO
        if answer == "Yes":
            print("It was "+ animal.name)
            self.is_won = True
            animal.propability = 1.0
            self.animals = [animal]
        else:
            animal.propability = 0.0
            self.normalizeAnimalPropability()
            self.removeUnlikelyAnimals()
            
    def askDifferentiatingQuestion(self):
        # pick a question
        question = self.getBestQuestion()
                
        # generate answer distribution for question
        answer_distribution_sum = dict()
        for label in question.labels:
            answer_distribution_sum[label.name] = 0.0
                
        for animal in self.animals:
            dist = animal.getAnswerDistribution(question.qid)
            for label in dist:
                answer_distribution_sum[label] += dist[label] 
                        
        for animal in self.animals:
            animal.normalized_answer_distribution = copy.deepcopy(animal.getAnswerDistribution(question.qid))
            for label in animal.normalized_answer_distribution:
                if not answer_distribution_sum[label] == 0:
                    animal.normalized_answer_distribution[label] /= answer_distribution_sum[label]

        # ask question and update propabilities based on response
        answer_label_name = question.ask(self.tts)
        
        for animal in self.animals:
            animal.propability *= animal.normalized_answer_distribution[answer_label_name]
                
        self.normalizeAnimalPropability()
        self.removeUnlikelyAnimals()
	
    def getBestQuestion(self):
        best_question = self.questions[0]
        for question in self.questions:
            question.updateScore(self.animals)
            if question.score > best_question.score:
                best_question = question

        return best_question
		
    def removeUnlikelyAnimals(self):
        new_animal = list()
        for animal in self.animals:
            if animal.propability > self.confidence_for_discard:
                new_animal.append(animal)
            else:
                print("Discarded " + animal.name 
                +". Relative propability was: " + str(animal.propability))
        self.animals = new_animal

        self.normalizeAnimalPropability()
		
    def normalizePropabilityList(self, propability_list):
        prop_sum = sum(propability_list)
		
        normalized_list = list()
        for prop in propability_list:
            normalized_list.append(1.0*prop/prop_sum)
			
        return normalized_list
		
    def normalizeAnimalPropability(self):
        propability_sum = 0.0
        for animal in self.animals:
            propability_sum += animal.propability
			
        if propability_sum <= 0.0:
            raise Exception('PropabilityError',"Diverged, total likelyhood sum is 0 or less.")
            
        for animal in self.animals:
            animal.propability /= propability_sum

    def buildAnimalsFromDatabase(self):
        animals = list()
        objects = self.loadJSON(self.animal_path)
        for obj in objects:
            try:
                animal = Animal(obj, self.questions)
                animals.append(animal)
            except (AssertionError):
                print("Failed to build an animal. Here is the "+
                "animal's JSON: "+ str(obj_dict))
            else:
                print("Added animal: " + animal.name)
        return animals

    def buildQuestionsFromDatabase(self):
        questions = list()
        objects = self.loadJSON(self.question_path)
        for obj_dict in objects:
            try:
                question = Question(obj_dict)
                questions.append(question)
            except(AssertionError):
                print("Failed to build a question. Here is the "+
                "question's JSON: "+ str(obj_dict))
            else:
                print("Added question with QID " + str(question.qid))
        return questions

    def loadJSON(self, path):
        objects = list()
        for object_file in os.listdir(path):
            if object_file.endswith(".json"):
                file_string = os.path.join(path, object_file)
                with open(file_string) as object_json:
                    try:
                        object_dict = json.load(object_json)
                    except(ValueError):
                        print("Failed to read JSON object: " + str(file_string))
                    else:
                        objects.append(object_dict)

        return objects
