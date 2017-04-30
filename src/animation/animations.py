# -*- encoding UTF-8 -*-

import sys
import math
from naoqi import ALProxy
import motion_dict


class Animations(object):

    def __init__(self, ip="127.0.0.1", port=9559):
        try:
            self.motion = ALProxy("ALMotion", ip, port)
        except Exception, error:
            print "Could not create proxy to ALMotion"
            print "Error was: ", error
            sys.exit(1)

    def face_palm(self):
        self.run(motion_dict.face_palm)

    def scratch_bum(self):
        self.run(motion_dict.scratch_bum)

    def tantrum(self):
        self.run(motion_dict.tantrum)

    def shake_head(self):
        self.run(motion_dict.shake_head)

    def nod_head(self):
        self.run(motion_dict.nod_head)

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

    def celebrate(self):
        self.run(motion_dict.celebrate)

    def wave(self):
        self.run(motion_dict.raise_right_arm)
        self.run(motion_dict.wave_right_arm)
        self.run(motion_dict.lower_right_arm)

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

    def __enter__(self):
        return self

    def __exit__(self, exec_type, exec_value, traceback):
        return


# Converts a lists of time intervals into a list of times
def intervals2times(intervals):
    n = len(intervals)
    times = [sum(intervals[0:i + 1]) for i in range(n)]
    return times

if __name__ == "__main__":
    a = Animations(port=35758)
    a.scratch_bum()
