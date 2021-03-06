import yaml
import os
import copy

from NaoModule import NaoModule

class ParameterServer(NaoModule):

    def __init__(self, name, top_level_config):
        NaoModule.__init__(self, name)

        # init attributes
        self.modules = dict()

        self.loadModule("naoParameterServer", top_level_config)
        for module_name in self.getParamNames():
            path = self.getParam(module_name)
            self.loadModule(module_name, path)
            
        self.logger.info(" Succesfully loaded " + str(len(self.modules))
                         + " modules.")

    def __exit__(self, exec_type, exec_value, traceback):
        for module in self.modules:
            self.saveModule(module)
        return

    # lambdas for the propper getters and setters for this module
    def getParam(self, param):
        return self.getParameter("naoParameterServer", param)

    def setParam(self, param, value):
        return self.setParameter("naoParameterServer", param, value)

    def getParamNames(self):
        return self.getParameterList("naoParameterServer")

    def getModuleList(self):
        """return a list of modules for which parameters are present"""
        return self.modules.keys()

    # get and set parameters
    def getParameterList(self, module_name):
        """
        """
        config = self.getModuleConfig(module_name)
        return config.keys()

    def getParameter(self, module_name, param):
        """
        """
        config = self.getModuleConfig(module_name)
        try:
            value = copy.deepcopy(config[param])
        except KeyError:
            self.logger.error("Parameter "+ param + " unknown in " +
                              "module " + module_name)
            return None
        else:
            return value

    def setParameter(self, module_name, parameter_name, value):
        """set a parameter in a module"""
        self.logger.debug(" In "+ module_name +
                          " changeing value " + parameter_name)

        config = self.getModuleConfig(module_name)

        try:
            config[parameter_name] = value
        except KeyError:
            self.logger.debug("Parameter " + parameter_name + "unknown.")
        else:
            self.saveModule(module_name)

    # axiliary functions
    def getModuleConfig(self, module_name):
        try:
            config = self.modules[module_name]
        except KeyError:
            self.logger.error("Module "+ module_name + " unknown.")
            return dict()
        else:
            return config

    def saveModule(self, module_name):
        self.logger.debug(" Saving Config file for " + module_name)

        config = self.getModuleConfig(module_name)
        
        location_parts = self.getParam(module_name)
        abs_path = self.getAbsPath(location_parts)
        with open(abs_path, 'w') as output:
            yaml.dump(config, output, default_flow_style=False)

    def loadModule(self, module_name, module_path):
        self.logger.info(" Loading Config for module: " + module_name)
        
        abs_path = self.getAbsPath(module_path)
        config = self.loadYAML(abs_path)

        if len(config) == 0:
            self.logger.warning(" Ignoring module: '" + module_name +"'\n"+
                                "No parameters specified.")
        else:
            self.modules[module_name] = config
            self.setParam(module_name, module_path)
            
            self.logger.info(" Added '" + module_name + "' config. " +
                              "It has " + str(len(config)) + " parameters.")

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
