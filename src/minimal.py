from NaoModule import NaoModule


class Minimal(NaoModule):

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

    # -------------------------------------
    # Overwritten from NaoModule
    # -------------------------------------
