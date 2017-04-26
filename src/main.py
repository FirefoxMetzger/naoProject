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

from core.GameModule import GameModule
from timer.timerModule import TimerModule
from parameter_server.naoParameterServer import naoParameterServer
from speechRecognition.speechModule import SpeechModule
from experimentLogger.ExperimentLogger import ExperimentLogger

def main():
    # initialize brooker
    naoProject = ALBroker("naoProject",
       "0.0.0.0",
       0,           # find free port
       MAIN_BROKER,
       MAIN_BROKER_PORT)
    
    # load framework classes
    
    #define global variables for all modules -- ugly but necessary (see naoqi documentation)
    global speech_module
    global timer_module
    global core
    global parameter_server
    global experiment_logger

    base_path = os.path.dirname(__file__)
    base_path = os.path.join(base_path , "..")

    rel_path = ["config","naoConfigServer.yaml"]
    
    with naoParameterServer("parameter_server", rel_path) as parameter_server,\
         SpeechModule("speech_module") as speech_module,\
         TimerModule("timer_module") as timer_module,\
         GameModule("core") as core, \
         ExperimentLogger("experiment_logger") as experiment_logger:

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
    (options, args) = parser.parse_args()

    if options.MAIN_BROKER:
        MAIN_BROKER = options.MAIN_BROKER
    if options.MAIN_BROKER_PORT:
        MAIN_BROKER_PORT = options.MAIN_BROKER_PORT

    main()
