from NaoModule import NaoModule


class SpeechModule(NaoModule):

    # -------------------------------------
    # Setup Module
    # -------------------------------------

    def __init__(self, name):
        NaoModule.__init__(self, name)

        #get Proxy handles
        self.getHandle("ALMemory")
        self.getHandle("ALTextToSpeech")
        self.getHandle("ALSpeechRecognition")
        self.getHandle("ALTouch")
        self.getHandle("ALDialog")

        #setup Proxy dependant stuff
        self.configureDialog()
        self.configureSpeechRecognition()

        #attributes
        self.menu_topics = list()

    def configureDialog(self):
        if self.hasHandle("ALDialog"):
            dialog = self.handles["ALDialog"]
            dialog.setLanguage("enu")
        else:
            self.logger.debug("Did not set up dialog.")

    def configureSpeechRecognition(self):
        if self.hasHandle("ALSpeechRecognition"):
            asr = self.handles("ALSpeechRecognition")
            asr.setVisualExpression(False)
            asr.setAudioExpression(False)
        else:
            self.logger.debug("Did not set up Speech Recognition.")

    # -------------------------------------
    # Callbacks
    # -------------------------------------

    def simpleMethod(self):
        """ Test Method """
        print "I have been bound and executed"

    def addMenuTopic(self, topic_path):
        """Try to load the given QiChat topic"""
        self.logger.debug("Adding QiChat topic %s" % topic_path)
        try:
            name = self.handles["ALDialog"].loadTopic(topic_path)
        except RuntimeError:
            self.logger.warning("Did not add topic from. From: %s" %\
                                (topic_path))
        else:
            self.menu_topics.append(name)
            self.logger.debug("Added topic %s" % (name))
            self.activateMenu()

    def activateMenu(self):
        """ activate all topics known to this module"""
        if self.hasHandle("ALDialog"):
            for topic_name in self.menu_topics:
                self.handles["ALDialog"].activateTopic(topic_name)
        else:
            self.logger.debug("Did not activate topics. No ALDialog module.")

    def deactivateMenu(self):
        """ deactivate all topics known to this module"""
        if self.hasHandle("ALDialog"):
            for topic in self.menu_topics:
                topic_name = topic["name"]
                self.handles["ALDialog"].deactivateTopic(topic_name)
        else:
            self.logger.debug("Did not deactivate topics. No ALDialog module.")

    # -------------------------------------
    # Overwritten from NaoModule
    # -------------------------------------

    def __enter__(self):
        if self.hasHandle("ALDialog"):
            self.handles["ALDialog"].subscribe(self.name)
        else:
            self.logger.debug("Did not subscribe to Dialog Manager.")
        return self

    def __exit__(self, exec_type, exec_value, traceback):
        if self.hasHandle("ALDialog"):
            dialog = self.handles["ALDialog"]
            dialog.unsubscribe(self.name)
            for topic in self.menu_topics:
                dialog.unloadTopic(topic)
        else:
            self.logger.debug("Could not free resources from Dialog Manager.")
        return

