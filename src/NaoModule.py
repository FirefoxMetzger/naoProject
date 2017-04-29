import logging
import os

from naoqi import ALModule
from naoqi import ALProxy

class NaoModule(ALModule):
    """
        This Class is sort of an abstract class.
        It serves as a base from which all modules in this project
        inherit.
    """
    
    def __init__(self, name):
        # call parent class constructor and store name
        ALModule.__init__(self, name)
        self.name = name

        # enable logging for each module
        logging.basicConfig()
        self.logger = logging.getLogger(self.name)
        self.logger.info("Logging enabled for: " + self.name)

        # get absolute path to root dir
        self.root_dir = os.path.dirname(__file__)
        self.root_dir = os.path.join(self.root_dir,'..')
        self.root_dir = os.path.abspath(self.root_dir)
        self.logger.debug("Base Path: " + str(self.root_dir))

        # variable to handle ALProxy handles
        self.handles = dict()

    def __enter__(self):
        # Allow calling this module using the with statement
        # modules may need to overwrite this to allocate resources
        return self

    def __exit__(self, exec_type, exec_value, traceback):
        # Allow calling this module using the with statement
        # modules may need to overwrite this to free resources
        return

    def hasAllHandles(self, module_names):
        #Helper function, to check if all Proxys are aviable
        has_all = True
        for module in module_names:
            has_all = ( has_all and self.hasHandle(module) )

    def hasHandle(self, module_name):
        #Helper function, to see if Proxy is aviable
        if module_name in self.handles.keys():
            return True
        else:
            return False

    def getHandle(self, module_name, is_critical=False):
        #get handle to proxy
        self.logger.debug("Getting module %s" % module_name)

        try:
            handle = ALProxy(module_name)
        except RuntimeError:
            if is_critical:
                self.logger.critical("Could not load module %s" % module_name)
                raise RuntimeError()
            else:
                self.logger.warning("Could not load module %s" % module_name)
        else:
            self.handles[module_name] = handle
            self.logger.debug("Added handle to %s" % module_name)

    

    def getAbsPath(self, chunks, alternate_dir=None):
        if alternate_dir is None:
            base_dir = self.root_dir
        else:
            base_dir = alternate_dir
        abs_path = base_dir
        for chunk in chunks:
            abs_path = os.path.join(abs_path,chunk)
        return abs_path
