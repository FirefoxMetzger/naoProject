
from Answer import Answer

class Animal:
    def __init__(self, animal_dict, questions=list()):
        try:
            self.name = animal_dict["name"]
        except (KeyError):
            raise AssertionError("The Dictionary needs a field called name specifying the animal's name")
        except (TypeError):
            raise AssertionError("The field 'name' is supposed to be a string.")
        
        self.answers = dict()
        try:
            assert "answers" in animal_dict
        except (AssertionError):
            animal_dict["answers"] = dict()
        
        for question in questions:
            self.answers[str(question.qid)] = question.getEmptyAnswer()
            try:
                frequency = animal_dict["answers"][str(question.qid)]
                self.answers[str(question.qid)].setLabelFrequency(frequency)
            except (KeyError):
                #the animal has no answer to this question 
                #- stick with the default values
                pass
            except (ValueError):
                #the animal's answer is malformated -- log it
                print("The stored answer to the question with QID "+str(question.qid)+" seems malformated.")
                print("It is omitted.")
            except (TypeError):
                print("There is something wrong with the format"+
                " of question: "+str(question.qid))
        
        # the game engine uses these to track if the user thinks of this animal
        self.propability = 1.0
        self.normalized_answer_distribution = dict()
		
    def getAnswerDistribution(self,qid):
        return self.answers[str(qid)].getDistribution()
            
    def getLabelPropability(self,qid,label_idx):
        return self.answers[str(qid)].getLabelPropability(label_idx)
