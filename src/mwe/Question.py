# A small file to get Mike to start working

import json

class Question:
    def __init__(self, path):
        json_data = open(path).read()
        answers = json.loads(json_data)
        self.distribution = answers["distribution"]
        self.ask_string = answers["string"]

    def getAnswerDistribution(self,idx):
        answer_distribution = []
        for obj in self.distribution:
            answer_distribution.append(obj[idx])

        return answer_distribution

    def getObjectDistribution(self,idx):
        print self.distribution[0]
        return self.distribution[idx]
