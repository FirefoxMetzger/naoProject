# -*- encoding UTF-8 -*-

import math
from NaoModule import NaoModule
import motions.motion_dict as motion_dict


class Animations(NaoModule):

    def __init__(self, name):
        NaoModule.__init__(self, name)
        self.getHandle("ALMotion")
        self.getHandle("ALMemory")
        self.motion = self.handles["ALMotion"]
        self.handles["ALMemory"].subscribeToEvent("QuestionAsked", self.name, "animation_callback")
        self.handles["ALMemory"].subscribeToEvent("NewGame", self.name, "animation_callback")
        self.handles["ALMemory"].subscribeToEvent("EndGame", self.name, "animation_callback")
        self.handles["ALMemory"].subscribeToEvent("GameEvent", self.name, "animation_callback")
        self.scratch_head()
        self.scratch_head()

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
        pass

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
        angle_lists = []
        for joint, angles in zip(* (motion["joints"], motion["angles"])):
            if "Hand" in joint:
                angle_lists.append(angles)
            else:
                angle_lists.append([math.radians(angle) for angle in angles])
        time_lists = [intervals2times(intervals) for intervals in motion["intervals"]]
        self.motion.angleInterpolation(motion["joints"], angle_lists, time_lists, True)


# Converts a lists of time intervals into a list of times
def intervals2times(intervals):
    n = len(intervals)
    times = [sum(intervals[0:i + 1]) for i in range(n)]
    return times

