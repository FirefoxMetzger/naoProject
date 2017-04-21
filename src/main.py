# -- NAO Project Main file --
# License: GPL
# Author: Sebastian Wallkoetter
# Email: sebastian@wallkoetter.net
#
# This file defines the entry point to the NAO game playing architecture.
# It loads games, handles the NAO's mood and is responsible for interrupting
# any part of the program.

import sys
import os.path
from optparse import OptionParser

from naoqi import ALBroker
from naoqi import ALProxy

from core.GameModule import GameModule
from timer.timerModule import TimerModule
from speechRecognition.speechModule import SpeechModule

def main():
    # get .ini file
    ini_filepath = ""
    ini_filename = "GameModule.conf"
    if not os.path.isfile(ini_filepath+ini_filename):
        print("could not find default .ini, please select")
        raise Exception("fileexception","The specified initialization file does not exist")

    # initialize brooker
    naoProject = ALBroker("naoProject",
       "0.0.0.0",
       0,           # find free port
       MAIN_BROKER,
       MAIN_BROKER_PORT)

    # load framework classes
    global speech_module
    speech_module = SpeechModule("speech_module")

    #define global variables for all modules -- ugly but necessary (see naoqi documentation)
    global question_module
    question_module = GameModule("question_module",ini_filepath,ini_filename)

    global timer_module
    timer_module = TimerModule("timer_module")

    # keep brooker alive
    try:
        while True:
            continue
    except KeyboardInterrupt:
        print
        print "interrupted -- shutting down"
        naoproject.shutdown()
        sys.exit(0)
                    
if __name__ == "__main__":
    MAIN_BROKER = "127.0.0.1"#"10.42.0.208"
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
