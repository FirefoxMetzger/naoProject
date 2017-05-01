import utility as util
import logging

from Answer import Answer

class Animal:
    def __init__(self, path, questions):
        logging.basicConfig()
        self.logger = logging.getLogger(__name__)
        self.logger.info("Logging enabled for: " + __name__)

        try:
            animal_dict = util.loadYAML(self, path)
        except AssertionError:
            self.logger.error("There was a problem loading question from %s" % path)

        try:
            self.name = str(animal_dict["name"])
        except (KeyError):
            raise AssertionError("The Dictionary needs a field called name specifying the animal's name")
        except (TypeError):
            raise AssertionError("The field 'name' is supposed to be a string.")
       
        self.text = str(animal_dict["text"])

        self.answers = dict()
        try:
            assert "answers" in animal_dict
        except (AssertionError):
            animal_dict["answers"] = dict()

        for question in questions:
            self.answers[question.qid] = question.getEmptyAnswer()
            try:
                self.logger.debug("Answer distribution: " +\
                    str(animal_dict["answers"][question.qid]))
                frequencies = animal_dict["answers"][question.qid]
                self.answers[question.qid].setLabelFrequency(frequencies)
            except (KeyError):
                #the animal has no answer to this question 
                #- stick with the default values
                pass
            except (ValueError):
                #the animal's answer is malformated -- log it
                self.logger.warn(\
                "The stored answer to the question with QID "+\
                str(question.qid) + " seems malformated." + \
                "It is omitted.")
            except (TypeError):
                self.logger.error("There is something wrong with the format"+
                " of question: "+str(question.qid))
        
        # the game engine uses these to track if the user thinks of this animal
        self.propability = 1.0
		
    def getAnswerDistribution(self,qid):
        return self.answers[qid].getDistribution()
            
    def getLabelPropability(self,qid,label_idx):
        return self.answers[qid].getLabelPropability(label_idx)
