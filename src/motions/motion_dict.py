#! /usr/bin/env python

raise_right_arm = {"joints": ["RShoulderPitch",
                              "RShoulderRoll",
                              "RElbowRoll",
                              "RElbowYaw",
                              "RWristYaw"],
                   "angles": [[-25],
                              [-20],
                              [50],
                              [110],
                              [-85]],
                   "intervals": [[1]] * 5}

lower_right_arm = {"joints": ["RShoulderPitch",
                              "RShoulderRoll",
                              "RElbowRoll",
                              "RElbowYaw",
                              "RWristYaw"],
                   "angles": [[85], [10], [23], [68], [-6]],
                   "intervals": [[1]] * 5}

shake_head = {"joints": ["HeadYaw"],
              "angles": [[20, -20, 20, -20, 20, -20, 0]],
              "intervals": [[0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2]]}

nod_head = {"joints": ["HeadPitch"],
            "angles": [[-5, 12, -5, 12, -5, 12, 0]],
            "intervals": [[0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.3]]}

wave_right_arm = {"joints": ["RShoulderRoll",
                             "RElbowYaw",
                             "RHand"],
                  "angles": [[20, -20, 20, -20],
                             [70, 110, 70, 110],
                             [1, 1, 1, 0.45]],
                  "intervals": [[0.7, 0.7, 0.7, 0.7]] * 3}

celebrate = {"joints": ["RShoulderPitch",
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
             "intervals": [[1, 0.5, 0.5, 0.5, 0.7, 1]] * 6}

face_palm = {"joints": ["HeadPitch",
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
                           [1, 1, 1]]}

scratch_bum = {"joints": ["RHand"],
               "angles": [[0.6, 1, 0, 1, 0, 1, 0.5]],
               "intervals": [[0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3]]}

scratch_head = {"joints": ["RShoulderPitch",
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
                              [1.1, 0.3, 0.3, 0.3, 0.3, 0.3, 0.6]]}

thinking_pose = {"joints": [],
                 "angles": [[]],
                 "intervals": [[]]}


template = {"joints": [],
            "angles": [[]],
            "intervals": [[]]}


template = {"joints": [],
            "angles": [[]],
            "intervals": [[]]}


template = {"joints": [],
            "angles": [[]],
            "intervals": [[]]}
