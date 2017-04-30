# -*- encoding UTF-8 -*-

import math
import almath
import motion as almotion
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
        self.handles["ALMemory"].subscribeToEvent("QuestionAsked", self.name, "animation_callback")
        self.handles["ALMemory"].subscribeToEvent("NewGame", self.name, "animation_callback")
        self.handles["ALMemory"].subscribeToEvent("EndGame", self.name, "animation_callback")
        self.handles["ALMemory"].subscribeToEvent("GameEvent", self.name, "animation_callback")

    def animation_callback(self, event_name, value):
        """
        """
        self.logger.debug("Animation callback executed.")
        if event_name == "QuestionAsked" and value == 1:
            pass
        elif event_name == "QuestionAsked" and value == 2:
            pass
        elif event_name == "QuestionAsked" and value == 3:
            pass
        elif event_name == "EndGame" and value == 0:
            self.face_palm()
        elif event_name == "EndGame" and value == 1:
            self.celebrate()
        elif event_name == "NewGame":
            pass
        elif event_name == "GameEvent":
            pass

    def face_palm(self):
        self.run(motion_dict.face_palm)

    def scratch_bum(self):
        pass

    def tantrum(self):
        self.leds.set_eyes('r')
        self.leds.eyes_on()
        self.posture.goToPosture("StandInit", 0.5)
        self.run(motion_dict.tantrum)
        self.posture.goToPosture("StandInit", 0.5)
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
        self.run(motion_dict.lower_right_arm)

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

    def run(self, motion):
        [self.motion.setStiffnesses(joint, 0.9) for joint in motion["joints"]]
        time_lists = [intervals2times(intervals) for intervals in motion["intervals"]]
        # time_lists = motion["intervals"]
        if motion["type"] == "angleInterpolation":
            angle_lists = deg2rad(motion["joints"], motion["angles"])
            self.motion.angleInterpolation(motion["joints"], angle_lists, time_lists, motion["is_absolute"])
        elif motion["type"] == "positionInterpolations":
            self.motion.positionInterpolations(motion["joints"], motion["space"], motion["path"],
                                               motion["axis_mask"], time_lists, motion["is_absolute"])
        else:
            print("Warning: unknown motion type: " + motion["type"])


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
