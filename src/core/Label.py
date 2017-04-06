

class Label:
    def __init__(self, label_dict):
        try:
            self.name = label_dict["name"]
        except(KeyError):
            raise AssertionError("The supplied label_dict does not have a field called 'name'")
        except(TypeError):
            raise AssertionError("The supplied label_dict doesn't appear to be a dictionary")            
