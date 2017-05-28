# naoProject
A repository holding data for the NAO Project for AINT512 at Plymouth University. 
This repo features software to enable the NAO to play 20 questions.
The application is developed in Python, but also uses QiChat and YAML.
It uses the NaoQi 1.14 bindings to comminicate with the robot.

It was deeloped by

* Sebastian Wallkoetter
* Samuel Westlake
* Michael Joannou

## Installation
1) Download the repository

    git clone https://github.com/FirefoxMetzger/naoProject.git

2) make sure you have installed pyYAML

    sudo apt install python-yaml
    
3) copy the topic files onto the robot (preferred destination: /home/nao/naoProject)

## License:
At the moment, this code is copyrighted by us. Simply, because it is still being marked by the Uni. Once that is done licence will change to some open source license.

## Brief Overview:

- analysis -- code used to do the study
- animals -- animals known to the game and their answer distribution
- config -- details for the parameter server
- experiment data -- the logs for the survey are stored here
- questions -- questions known to the games, asked by the robot
- src -- the actual code ordered by modules
- topics -- QiChat topics for the game and menu (need to be copied to the robot)
