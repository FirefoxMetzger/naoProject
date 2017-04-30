# -- NAO Project Main file --
# License: GPL
# Author: Sebastian Wallkoetter
# Email: sebastian@wallkoetter.net
#
# This file defines the entry point to the NAO game playing architecture.
# It loads games, handles the NAO's mood and is responsible for interrupting
# any part of the program.

import sys
import os
from optparse import OptionParser

from naoqi import ALBroker
from naoqi import ALProxy

from ParameterServer import ParameterServer
from LEDs import LEDs
from Animations import Animations
from ExperimentLogger import ExperimentLogger
from MoodModule import MoodModule
from SpeechModule import SpeechModule
from TimerModule import TimerModule
from GameModule import GameModule
from minimal import Minimal

def main(is_on_robot):
    # initialize brooker
    naoProject = ALBroker("naoProject",
       "0.0.0.0",
       0,           # find free port
       MAIN_BROKER,
       MAIN_BROKER_PORT)
    
    # load framework classes
    
    #define global variables for all modules -- ugly but necessary (see naoqi documentation)
    global mood
    global speech_module
    global timer_module
    global game_module
    global parameter_server
    global experiment_logger
    global leds
    global animations

    base_path = os.path.dirname(__file__)
    base_path = os.path.join(base_path , "..")

    rel_path = ["config", "naoConfigServer.yaml"]

    with ParameterServer("parameter_server", rel_path) as parameter_server,\
         SpeechModule("speech_module") as speech_module,\
         LEDs("leds") as leds,\
         Animations("animations") as animations,\
         MoodModule("mood") as mood, \
         TimerModule("timer_module", is_on_robot) as timer_module,\
         GameModule("game_module", is_on_robot) as game_module,\
         ExperimentLogger("experiment_logger") as experiment_logger:
         
        trigger_finger = ALProxy("ALMemory")
        trigger_finger.raiseEvent("emoBlink", 3000)

        # keep brooker alive
        try:
            while True:
                continue
        except KeyboardInterrupt:
            print
            print "interrupted -- shutting down"
    naoProject.shutdown()
    sys.exit(0)
                    
if __name__ == "__main__":
    MAIN_BROKER = "127.0.0.1"
    MAIN_BROKER_PORT = 9559

    parser = OptionParser()
    parser.add_option("--IP",type="string",dest="MAIN_BROKER")
    parser.add_option("-p","--PORT",type="int",dest="MAIN_BROKER_PORT")
    parser.add_option("--on-robot", action="store_true", dest="IS_ON_ROBOT", default=False)
    (options, args) = parser.parse_args()

    if options.MAIN_BROKER:
        MAIN_BROKER = options.MAIN_BROKER
    if options.MAIN_BROKER_PORT:
        MAIN_BROKER_PORT = options.MAIN_BROKER_PORT

    main(options.IS_ON_ROBOT)
