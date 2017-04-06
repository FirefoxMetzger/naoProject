import ConfigParser

from naoqi import ALProxy
from naoqi import ALModule

from Game import Game

class GameModule(ALModule):
    """ A simple module able to react
    to facedetection events

    """
    def __init__(self, name, config_path="", config_file="GameModule.conf"):
        ALModule.__init__(self, name)

        self.config = ConfigParser.ConfigParser()
        self.config.read(config_path+config_file)

        # init text to speach proxy
        self.tts = ALProxy("ALTextToSpeech")
        self.tts.setLanguage("English")
        self.tts.setParameter("speed", self.config.getfloat("TTS","Speed"))
        self.tts.setParameter("pitchShift", self.config.getfloat("TTS","Pitch"))
        self.tts.setVolume(self.config.getfloat("TTS","Volume"))
        
        self.name = name
        self.game = Game(self.config, self.tts)
        
        # Subscribe to the FaceDetected event:
        global memory
        memory = ALProxy("ALMemory")
        memory.subscribeToEvent("FaceDetected",
            self.name,
            "onFaceDetected")
			
        memory.subscribeToEvent("MiddleTactilTouched",
            self.name,
            "onTouched")
			
    def onTouched(self, strVarName, value):
        """ This will be called each time a touch is detected
        
        """

        if value == 0:
            #button up -- don't react
            return

        memory.unsubscribeToEvent("MiddleTactilTouched",
                self.name)
       
        self.gameTurn()

        # Subscribe again to the event
        memory.subscribeToEvent("MiddleTactilTouched",
            self.name,
            "onTouched")
	
    def gameTurn(self):
        self.game.loop()
        
        if self.game.is_won:
            self.tts.say("This was to easy.")
            self.gameAftermath()
            
        if self.game.number_of_questions <= self.game.num_asked:
            self.tts.say("Damn! You are to good for me.")
            self.gameAftermath()
            
    def gameAftermath(self):
        #self.tts.say("I will remember your animal.")
        self.tts.say("If you want to play again, simply touch my head.")
        self.game = Game(self.config, self.tts)

    def onFaceDetected(self, value, subscriberIdentifier):
        """ This will be called each time a face is
        detected.

        """
        # Unsubscribe to the event when talking,
        # to avoid repetitions
        memory.unsubscribeToEvent("FaceDetected",
            self.name)

        self.tts.say("You there. Fuck off! You are blocking my view.")

        # Subscribe again to the event
        memory.subscribeToEvent("FaceDetected",
            self.name,
            "onFaceDetected")
