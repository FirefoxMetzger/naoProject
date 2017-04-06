
import random

from Answer import Answer
from Label import Label

class Question:
    def __init__(self,question_dict):
        try:
            self.say_string = question_dict["say_string"]
        except (KeyError):
            raise AssertionError("A question must supply a string for the NAO to say")
            
        try:
            self.qid = question_dict["qid"]
        except (KeyError):
            raise AssertionError("A question must supply a (unique) QID")       
		
        try:
            assert "labels" in question_dict
        except (AssertionError):
            raise AssertionError("A question must supply answer categories -- no 'labels' provided")
        
        self.labels = list()
        for label_dict in question_dict["labels"]:
            self.labels.append(Label(label_dict))
        self.score = 0
        
        #TODO add fields needed for speech recognition
		
    def updateScore(self, animals):
        avg_propability = 1.0 / len(self.labels)
        answers = [animal.answers[str(self.qid)] for animal in animals]

        seperation_score = 0.0
        total_dist = dict()
        for label in self.labels:
            total_dist[label.name] = 0.0

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
            label_names.append(label.name)
        answer = Answer(label_names)
        return answer

    def ask(self, tts):
        print(str(self.say_string))
        tts.say(str(self.say_string))
        return self.labels[1].name
