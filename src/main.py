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

from naoqi import ALBroker
from naoqi import ALProxy
from naoqi import ALModule

from core.GameModule import GameModule

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
	

    #define global variables for all modules -- ugly but necessary (see naoqi documentation)
    global question_game
    question_game = GameModule("question_game",ini_filepath,ini_filename)

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
    MAIN_BROKER_PORT = 45441
    previous_argument = ""
    for arg in sys.argv:
        if previous_argument == "--ip":
            MAIN_BROKER = int(arg)
        elif previous_argument == "--port":
            MAIN_BROKER_PORT = int(arg)
        previous_argument = arg
    main()
