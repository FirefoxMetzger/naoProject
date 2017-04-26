import json
import yaml
import os

def getAbsPath(base_path, chunks):
    abs_path = base_path
    for chunk in chunks:
        abs_path = os.path.join(abs_path,chunk)
    return abs_path

def loadJSON( path):
    with open(path, 'r') as stream:
        try:
            object_dict = json.load(stream)
        except(ValueError):
            print("Failed to read JSON object: " + str(path))
            object_dict = None
            
    return object_dict or dict()

def loadYAML(self, path):
    self.logger.debug(" Loading YAML at: " + path)
    try:
        stream = open(path, 'r')
    except IOError:
        self.logger.error(" Could not open config file at: \n"+
                     os.path.abspath(path) + "\n"
                     " No such file.")
        return dict()
    else:
        with stream:
            config = None
            try:
                config = yaml.safe_load(stream.read())
                assert(type(config) == dict)
            except yaml.YAMLError as exc:
                self.logger.error(exc)
                config = None
            except AssertionError:
                self.logger.error("Parsed YAML is not a dict. \n" +
                                  "In " + os.path.abspath(path))
                config = None
            finally:
                config = config or dict()
    return config
