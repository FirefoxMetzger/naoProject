

class Answer:
    def __init__(self,label_names):
        self.labelPropability = dict()
        self.frequency = dict()
        for name in label_names:
            self.labelPropability[name] = 0.0
            self.frequency[name] = 0
            
        self.normalize()
			
    def getDistribution(self):
        return self.labelPropability
		
    def getLabelPropability(self, label):
        if label in self.labelPropability:
            return self.labelPropability[label]
        else:
            raise Exception('UndefinedLabel','The answer has not been initialized properly')
            
    def setLabelFrequency(self, frequencies):
        old_frequency = dict()
        for label in self.frequency:
            try:
                freq = frequencies[label]
            except (KeyError):
                # revert changes and say that it doesn't work
                for label, freq in old_frequency:
                    self.frequency[label] = freq
                raise ValueError("One of the labels doesn't have a matching frequency")
            
            old_frequency[label] = self.frequency[label]
            self.frequency[label] = freq
            
        self.normalize()
            
    def normalize(self):
        dist_sum = 0.0
        num_keys = 0.0
        
        for key in self.frequency:
            dist_sum += self.frequency[key]
            num_keys += 1.0
            
        if dist_sum == 0.0:
            for key in self.labelPropability:
                self.labelPropability[key] = 1.0 / num_keys
        else:
            for key in self.labelPropability:
                self.labelPropability[key] = self.frequency[key] / dist_sum
