# -- NAO Project Main file --
# License: GPL
# Author: Sebastian Wallkoetter
# Email: sebastian@wallkoetter.net
#
# This file is the main file to handle the 20 questions game.

class question_game:
    MAX_QUESTIONS = 20
    MIN_GUESSES = 3

    def __init__:
        self.is_won = False
        self.num_questions_asked = 0
        self.known_objects = 0 #TODO: replace with list of objects


    def main_loop():
        self.resetAllScores()

        for question_counter in range(1,MAX_QUESTIONS):
            is_correct = False
            num_ties = self.getNumberOfTiedScores()

            if MAX_QUESTIONS - self.num_questions_asked == MIN_GUESSES:
                #no more questions -- start guessing
                is_correct = self.askHighestObject()

            elif num_ties < MAX_QUESTIONS - self.num_questions_asked:
                #stop differentiating, just guess from here
                is_correct = self.askHighestObject()
            else:
                #to many options try to differentiate more
                self.differentiateFurther()
            
            self.num_questions_asked += 1

            if is_correct:
                self.is_won = True
                break;

        if self.is_won:
            self.game_won()
        else:
            self.game_lost()
        return

    def askHighestObject():
        return False

    def differentiateFurther():
        next_question_idx = self.bestQuestionIdx()
        response = self.askQuestion(next_question_idx)
        self.adjustScores(response)
        return

    def bestQuestionIdx():
        return 1

    def adjustScores(response):
        return

    def getNumberOfTiedScores():
        return

    def game_won():
        return

    def game_lost():
        return

    def askQuestion(next_question_idx):
        return
