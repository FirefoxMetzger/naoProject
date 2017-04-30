import random
import logging
from naoqi import ALProxy

from Answer import Answer
import utility as util

class Question:
    def __init__(self,path):
        logging.basicConfig()
        self.logger = logging.getLogger(__name__)
        self.logger.info("Logging enabled for: " + __name__)

        self.memory = ALProxy("ALMemory")
        self.speech = ALProxy("speech_module")
        self.tts = ALProxy("ALTextToSpeech")

        question_dict = util.loadYAML(self, path)

        self.text = str(question_dict["text"])
        self.labels = question_dict["labels"]
        self.topic = question_dict["topic"]
        self.qid = question_dict["QID"]
        self.topic_name = str(question_dict["topic_name"])

        self.score = 0

    def activate(self):
        for label in self.labels:
            self.memory.subscribeToEvent(str(label), "game_module", "AskedQuestionCallback")

    def deactivate(self):
        for label in self.labels:
            self.memory.unsubscribeToEvent(str(label), "game_module")

    def updateScore(self, animals):
        avg_propability = 1.0 / len(self.labels)
            
        # answer distribution for this question
        answers = [animal.answers[self.qid] for animal in animals]
                   
        # distribution over labels
        label_distribution = dict()
        prop_sum = dict()
        for label in answers[0].labelPropability:
            prop_sum[label] = sum([answer.labelPropability[label] for answer in answers])
            label_distribution[label] = 1.0 * prop_sum[label] / len(answers)
            
        for answer in answers:
            answer.setRelativePropability(prop_sum)
        
        discarded_per_label = dict()
        for label in label_distribution.keys():
            animals_discarded = list()
            for animal in animals:
                if animal.propability * animal.answers[self.qid].relativeLabelPropability[label] <= 0.05:
                    animals_discarded.append(1)
            discarded_per_label[label] = sum(animals_discarded)
            
        self.score = 0
        for label in label_distribution.keys():
            self.score += label_distribution[label] * discarded_per_label[label]
            
        print("Average animals discarded for question %s: %f" % (self.qid, self.score))
                
    def getEmptyAnswer(self):
        label_names = list()
        for label in self.labels:
            label_names.append(label)
        answer = Answer(label_names)
        return answer

    def ask(self):
        self.tts.say(self.text)
        print(self.text)
        
