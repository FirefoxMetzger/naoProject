# A small script that enabels everybody to work on their features

from Question import Question
from Animal import Animal
import random

class QuestionGame:
    def __init__(self):
        #define your dependancies here
        self.questions = []
        self.questions.append(Question("question_test.json"))
        self.questions.append(Question("dog.json"))

        animal_list = ["cat","dog","bird"]
        self.animals = []
        for animal_name in animal_list:
            self.animals.append(Animal(animal_name))
        
        self.belief = []
        for animal in self.animals:
            self.belief.append(1)

        return

    # return: boolean - true if game is won
    def loop(self):
        for question_number in range (1,20):
            question_idx = self.selectQuestion()
            self.askQuestion(self.questions[question_idx])

            if not self.normalize_belief():
                print ("I don't know the animal")
                return False
            
            for animal in self.animals:
                if animal.propability > 0.9:
                    print("It is a " + animal.name)
                    return True

        else:
            return False

    def askQuestion(self, question):
        print (question.ask_string)
        
        return_value = raw_input("'Yes' or 'No'? ")
        if return_value == "Yes":
            answer_dist = question.getAnswerDistribution(0)
        else:
            answer_dist = question.getAnswerDistribution(1)

        for idx in range(0,len(self.animals)):
            self.animals[idx].propability *= answer_dist[idx]

        return

    def selectQuestion(self):
        return random.randint(0,1)

    # return false if it fails
    def normalize_belief(self):
        array_sum = 0
        for animal in self.animals:
            array_sum += animal.propability

        if array_sum == 0:
            return False
        else:
            for animal in self.animals:
                animal.propability /= array_sum

        return True


    # the nao has just won a game
    def naoWon(self):
        return

    #the nao has just lost a game
    def naoLost(self):
        return
    
def main():
    game = QuestionGame()
    b_nao_won = game.loop()

    if b_nao_won:
        game.naoWon()
    else:
        game.naoLost()

if __name__ == "__main__":
    main()
