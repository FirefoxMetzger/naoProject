# -*- encoding UTF-8 -*-

import math
import random
import time
from NaoModule import NaoModule
import motions.motion_dict as motion_dict


class Animations(NaoModule):

    def __init__(self, name):
        NaoModule.__init__(self, name)
        self.getHandle("leds")
        self.getHandle("ALMotion")
        self.getHandle("ALMemory")
        self.getHandle("ALRobotPosture")
        self.motion = self.handles["ALMotion"]
        self.posture = self.handles["ALRobotPosture"]
        self.leds = self.handles["leds"]
        self.handles["ALMemory"].subscribeToEvent("QuestionAsked", self.name, "question_asked_cb")
        self.handles["ALMemory"].subscribeToEvent("NewGame", self.name, "new_game_cb")
        self.handles["ALMemory"].subscribeToEvent("EndGame", self.name, "end_game_cb")
        self.handles["ALMemory"].subscribeToEvent("GameEvent", self.name, "game_event_cb")

    def question_asked_cb(self, event_name, value):
        """
        """
        self.logger.debug("Animation callback executed.")
        if value == "fly":
            self.flap()
        elif value == "this":
            self.this_big()

    def end_game_cb(self, event_name, value):
        """
        """
        if value == 0:
            chance = random.randrange(0, 2)
            if chance == 0:
                self.face_palm()
            elif chance == 1:
                self.tantrum()
        elif value == 1:
            chance = random.randrange(0, 2)
            if chance == 0:
                self.celebrate()
            elif chance == 1:
                self.arms_up()

    def new_game_cb(self, event_name, value):
        """
        """
        pass

    def game_event_cb(self, event_name, value):
        """
        """
        if value[0] != "guess":
            chance = random.randrange(0, 3)
            if chance == 0:
                self.thinking_pose()
            elif chance == 1:
                self.scratch_head()

    def this_big(self):
        self.run(motion_dict.this_big)
        self.posture.goToPosture("Stand", 0.5)

    def face_palm(self):
        self.run(motion_dict.face_palm)

    def arms_up(self):
        self.run(motion_dict.arms_up)
        self.posture.goToPosture("Stand", 1)

    def scratch_bum(self):
        pass

    def flap(self):
        self.run(motion_dict.flap)
        self.posture.goToPosture("Stand", 0.5)

    def tantrum(self):
        self.leds.set_eyes('r')
        self.leds.eyes_on()
        self.posture.goToPosture("StandInit", 0.5)
        self.run(motion_dict.tantrum)
        self.posture.goToPosture("Stand", 0.5)
        self.leds.set_eyes('w')
        self.leds.eyes_on()

    def shake_head(self):
        self.run(motion_dict.shake_head)

    def scratch_head(self):
        self.run(motion_dict.scratch_head)
        self.run(motion_dict.lower_right_arm)

    def nod_head(self):
        self.run(motion_dict.nod_head)

    def celebrate(self):
        self.run(motion_dict.celebrate)

    def wave(self):
        self.run(motion_dict.raise_right_arm)
        self.run(motion_dict.wave_right_arm)
        self.posture.goToPosture("Stand", 1.0)

    def thinking_pose(self):
        self.run(motion_dict.thinking_pose)
        self.run(motion_dict.lower_right_arm)

    def right_hand(self, pos, time):
        self.motion.setStiffnesses("RHand", 0.9)
        self.motion.angleInterpolation("RHand", pos, time, True)

    def left_hand(self, pos, time):
        self.motion.setStiffnesses("LHand", 0.9)
        self.motion.angleInterpolation("LHand", pos, time, True)

    def hands(self, pos, time):
        self.motion.setStiffnesses("LHand", 0.9)
        self.motion.setStiffnesses("RHand", 0.9)
        self.motion.angleInterpolation(["LHand", "RHand"], [pos] * 2, [time] * 2, True)

    def run(self, motion, post=False):
        [self.motion.setStiffnesses(joint, 0.9) for joint in motion["joints"]]
        time_lists = [intervals2times(intervals) for intervals in motion["intervals"]]
        if motion["type"] == "angleInterpolation":
            angle_lists = deg2rad(motion["joints"], motion["angles"])
            if post:
                self.motion.post.angleInterpolation(motion["joints"], angle_lists,
                                                              time_lists, motion["is_absolute"])
            else:
                self.motion.angleInterpolation(motion["joints"], angle_lists,
                                               time_lists, motion["is_absolute"])
        elif motion["type"] == "positionInterpolations":
            if post:
                self.motion.post.positionInterpolations(motion["joints"], motion["space"], motion["path"],
                                                                  motion["axis_mask"], time_lists, motion["is_absolute"])
            else:
                self.motion.positionInterpolations(motion["joints"], motion["space"], motion["path"],
                                                   motion["axis_mask"], time_lists, motion["is_absolute"])
        else:
            print("Warning: unknown motion type: " + motion["type"])

    def demo(self):
        self.flap()
        self.face_palm()
        self.arms_up()
        self.this_big()
        self.scratch_head()
        self.tantrum()
        self.wave()
        self.thinking_pose()


# Converts a lists of time intervals into a list of times
def intervals2times(intervals):
    n = len(intervals)
    times = [sum(intervals[0:i + 1]) for i in range(n)]
    return times


# Convert lists of angles into radians
def deg2rad(joints, angles_deg):
    angle_lists = []
    for joint, angles in zip(*(joints, angles_deg)):
        if "Hand" in joint:
            angle_lists.append(angles)  # Do not convert to radians
        else:
            angle_lists.append([math.radians(angle) for angle in angles])  # Convert to radians
    return angle_lists
