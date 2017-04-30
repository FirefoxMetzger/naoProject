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
        answers = [animal.answers[self.qid] for animal in animals]

        seperation_score = 0.0
        total_dist = dict()
        for label in self.labels:
            total_dist[label] = 0.0

        for answer in answers:
            for label in answer.labelPropability:
                total_dist[label] += answer.labelPropability[label]

        for label in total_dist:
            seperation_score += abs(total_dist[label] / len(self.labels) - avg_propability)

        seperation_score = 50 - seperation_score

        decided_score = 0.0
        for answer in answers:
            for label in answer.labelPropability:
                decided_score += abs(answer.labelPropability[label] - avg_propability)

        exploration_score = random.random() * 10;

        print(str(seperation_score) + " + " + str(decided_score) + " + " + str(exploration_score))
        self.score = seperation_score + decided_score + exploration_score;
                
    def getEmptyAnswer(self):
        label_names = list()
        for label in self.labels:
            label_names.append(label)
        answer = Answer(label_names)
        return answer

    def ask(self):
        self.tts.say(self.text)
        print(self.text)
        
