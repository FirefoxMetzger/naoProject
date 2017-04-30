#! /usr/bin/env python

import almath
import motion

raise_right_arm = {"type": "angleInterpolation",
                   "joints": ["RShoulderPitch",
                              "RShoulderRoll",
                              "RElbowRoll",
                              "RElbowYaw",
                              "RWristYaw"],
                   "angles": [[-25],
                              [-20],
                              [50],
                              [110],
                              [-85]],
                   "intervals": [[1]] * 5,
                   "is_absolute": True}

lower_right_arm = {"type": "angleInterpolation",
                   "joints": ["RShoulderPitch",
                              "RShoulderRoll",
                              "RElbowRoll",
                              "RElbowYaw",
                              "RWristYaw"],
                   "angles": [[85], [10], [23], [68], [-6]],
                   "intervals": [[1.2]] * 5,
                   "is_absolute": True}

shake_head = {"type": "angleInterpolation",
              "joints": ["HeadYaw"],
              "angles": [[20, -20, 20, -20, 20, -20, 0]],
              "intervals": [[0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2]],
              "is_absolute": True}

nod_head = {"type": "angleInterpolation",
            "joints": ["HeadPitch"],
            "angles": [[-5, 12, -5, 12, -5, 12, 0]],
            "intervals": [[0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.3]],
            "is_absolute": True}

wave_right_arm = {"type": "angleInterpolation",
                  "joints": ["RShoulderRoll",
                             "RElbowYaw",
                             "RHand"],
                  "angles": [[20, -20, 20, -20],
                             [70, 110, 70, 110],
                             [1, 1, 1, 0.45]],
                  "intervals": [[0.7, 0.7, 0.7, 0.7]] * 3,
                  "is_absolute": True}

celebrate = {"type": "angleInterpolation",
             "joints": ["RShoulderPitch",
                        "RShoulderRoll",
                        "RElbowRoll",
                        "RElbowYaw",
                        "RWristYaw",
                        "RHand"],
             "angles": [[-17, 32, 3, 32, 32, 85],
                        [14, 10, 7, 10, 10, 10],
                        [55, 88, 70, 88, 88, 23],
                        [95, 88, 88, 88, 88, 68],
                        [70, 91, 91, 91, 91, -6],
                        [1, 0, 0, 0, 0, 0.45]],
             "intervals": [[1, 0.5, 0.5, 0.5, 0.7, 1]] * 6,
             "is_absolute": True}

face_palm = {"type": "angleInterpolation",
             "joints": ["HeadPitch",
                        "HeadYaw",
                        "RShoulderPitch",
                        "RShoulderRoll",
                        "RElbowRoll",
                        "RElbowYaw",
                        "RWristYaw",
                        "RHand"],
             "angles": [[20, 20, 0],
                        [20, -20, 20, -20, 0],
                        [23, 23, 85],
                        [18, 18, 10],
                        [83, 83, 24],
                        [50, 50, 69],
                        [62, 62, -6],
                        [1, 1, 0.45]],
             "intervals": [[1.5, 1, 0.3],
                           [0.2, 0.4, 0.4, 0.4, 0.2],
                           [1, 1, 1],
                           [1, 1, 1],
                           [1, 1, 1],
                           [1, 1, 1],
                           [1, 1, 1],
                           [1, 1, 1]],
             "is_absolute": True}

scratch_bum = {"type": "angleInterpolation",
               "joints": ["RHand"],
               "angles": [[0.6, 1, 0, 1, 0, 1, 0.5]],
               "intervals": [[0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3]],
               "is_absolute": True}

scratch_head = {"type": "angleInterpolation",
                "joints": ["RShoulderPitch",
                           "RShoulderRoll",
                           "RElbowRoll",
                           "RElbowYaw",
                           "RWristYaw",
                           "RHand"],
                "angles": [[-24, -24],
                           [-18.5, -18.5],
                           [88.5, 88.5],
                           [45.5, 45.5],
                           [60, 60],
                           [0.45, 0.2, 0.7, 0.2, 0.7, 0.2, 0.45]],
                "intervals": [[1, 1.6],
                              [1, 1.6],
                              [1, 1.6],
                              [1, 1.6],
                              [1, 1.6],
                              [1.1, 0.3, 0.3, 0.3, 0.3, 0.3, 0.6]],
                "is_absolute": True}

thinking_pose = {"type": "angleInterpolation",
                 "joints": ["RShoulderPitch",
                            "RShoulderRoll",
                            "RElbowRoll",
                            "RElbowYaw",
                            "RWristYaw",
                            "RHand"],
                 "angles": [[40.2, 40.2],
                            [18, 18],
                            [88.5, 88.5],
                            [40, 40],
                            [88, 88],
                            [0.35, 0.35, 0.5]],
                 "intervals": [[1, 2],
                               [1, 2],
                               [1, 2],
                               [1, 2],
                               [1, 2],
                               [1, 2.5, 0.5]],
                 "is_absolute": True}


tantrum = {"type": "positionInterpolations",
           "joints": ["LLeg", "RLeg"],
           "space": motion.FRAME_WORLD,
           "path": [[[0.0, 0.0, 0.005, 0.0, 0.0, 0.0],
                     [0.0, 0.0, -0.005, 0.0, 0.0, 0.0],
                     [0.0, 0.0, 0.005, 0.0, 0.0, 0.0],
                     [0.0, 0.0, -0.005, 0.0, 0.0, 0.0],
                     [0.0, 0.0, 0.005, 0.0, 0.0, 0.0],
                     [0.0, 0.0, -0.005, 0.0, 0.0, 0.0],
                     [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]],
                    [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                     [0.0, 0.0, 0.005, 0.0, 0.0, 0.0],
                     [0.0, 0.0, -0.005, 0.0, 0.0, 0.0],
                     [0.0, 0.0, 0.005, 0.0, 0.0, 0.0],
                     [0.0, 0.0, -0.005, 0.0, 0.0, 0.0],
                     [0.0, 0.0, 0.005, 0.0, 0.0, 0.0],
                     [0.0, 0.0, -0.005, 0.0, 0.0, 0.0]]],
           "axis_mask": [almath.AXIS_MASK_ALL] * 2,
           "intervals": [[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]] * 2,
           "is_absolute": False}


template = {"joints": [],
            "angles": [[]],
            "intervals": [[]]}


template = {"joints": [],
            "angles": [[]],
            "intervals": [[]]}
