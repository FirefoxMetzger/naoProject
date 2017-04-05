# -*- encoding UTF-8 -*-

import sys 
from time import sleep
from math import radians
from naoqi import ALProxy
from lib.groups import *
from multiprocessing import Process


class Animations(object):

	def __init__(self, ip, port=9559):
		try: 
			self.motion = ALProxy("ALMotion", ip, port)
		except Exception, e:
			print "Could not create proxy to ALMotion"
			print "Error was: ", e
			sys.exit(1)									# System exit and return 1
		try: 
			self.leds = ALProxy("ALLeds", ip, port)
		except Exception, e:
			print "Could not create proxy to ALMotion"
			print "Error was: ", e
			sys.exit(1)									# System exit and return 1
		self._create_groups()

	# Create groups of LEDs
	def _create_groups(self):
		# Eye groups
		self.leds.createGroup("top_left", top_left)				# Top LED in left eye (RGB)
		self.leds.createGroup("upper_left", upper_left)			# Upper 2 LEDs in left eye (RGB)
		self.leds.createGroup("middle_left", middle_left)		# Middle LEDs in left eye (RGB)
		self.leds.createGroup("lower_left", lower_left)			# Lower LEDs in left eye (RGB)
		self.leds.createGroup("bottom_left", bottom_left)		# Bottom LED in left eye (RGB)
		self.leds.createGroup("top_right", top_right)			# Top LED in right eye (RGB)
		self.leds.createGroup("upper_right", upper_right)		# Upper LEDs in right eye (RGB)
		self.leds.createGroup("middle_right", middle_right)		# Middle LEDs in right eye (RGB)
		self.leds.createGroup("lower_right", lower_right)		# Lower LEDs in right eye (RGB)
		self.leds.createGroup("bottom_right", bottom_right)		# Bottom LED in right eye (RGB)
		self.leds.createGroup("top", top)						# Top LEDs in both eyes (RGB)
		self.leds.createGroup("upper", upper)					# Upper LEDs in both eyes (RGB)
		self.leds.createGroup("middle", middle)					# Middle LEDs in both eyes (RGB)
		self.leds.createGroup("lower", lower)					# Lower LEDs in both eyes (RGB)
		self.leds.createGroup("red", red)						# All red eye LEDs
		self.leds.createGroup("green", green)					# All green eye LEDs
		self.leds.createGroup("blue", blue)						# All blue eye LEDs
		# Ear groups
		self.leds.createGroup("bottom", bottom)					# Bottom LEDs in both eyes (RGB)
		self.leds.createGroup("ears", ears)						# All ear LEDs

	# Make NAO shake its head from side to side
	def shake_head(self, n=3, yaw=20, time=0.5, pitch=0, pause=0.1, reset_time=0.1, exe=True):
		# <n> = number of shakes
		# <yaw> = maximum yaw angle of the nod
		# <time> = number of seconds per nod
		# <pitch> = final pitch angle of the action
		# <pause> = seconds before resetting head to default position (when pitch != 0)
		# <rest_time> = seconds required to reset head (when pitch != 0)
		# <exe> = if true, the movement will be executed (for use when combining movement)
		yaw = radians(yaw)												
		pitch = radians(pitch)
		self.motion.setStiffnesses("Head", 0.9)							# Set stiffness
		is_absolute = True												# Set movements to absolute (not relative)				
		joints = ["HeadYaw", "HeadPitch"]								# Joints to control
		yaw_angles = [yaw * (-1) ** i for i in range(n)] + [0] 			# Series of yaw angles 
		yaw_intervals = [time / 2.0] + [time] * (n-1) + [time / 2.0]	# Time interval for each movement
		yaw_times = intervals2times(yaw_intervals) 						# Times for each movement
		pitch_angles = [pitch, pitch, 0] 								# Serie of pitch angles 
		pitch_intervals = [yaw_times[-1], pause, reset_time] 			# Time intervals for each movement
		pitch_times = intervals2times(pitch_intervals) 					# Times for each movement
		angle_lists = [yaw_angles, pitch_angles]						# Complete list of all angles to move to
		time_lists = [yaw_times, pitch_times]							# Complte list of all times for each angle
		if exe:
			self.motion.angleInterpolation(joints, angle_lists, time_lists, is_absolute) 	# GO! 
		return joints, angle_lists, time_lists

	# Make NAO nod its head up and down
	def nod_head(self, n=2, pitch=(-10, 20), time=0.5):
		# <n> = number of nods 
		# <pitch> = tuple containing the min and max pitch angle of the nod 
		# <time> = number of seconds for each nod
		self.motion.setStiffnesses("Head", 0.9)											# Set stiffness
		is_absolute = True																# Set motion to absolute
		joint = "HeadPitch"																# Joint to control
		pitch_angles = [radians(pitch[0]), radians(pitch[1])] * n + [0] 				# List of target pitch angles
		pitch_intervals = [time / 2.0 ] * (n * 2 + 1)									# List if time intervals for each motion
		pitch_times = intervals2times(pitch_intervals) 									# List of time for each motion
		self.motion.angleInterpolation(joint, pitch_angles, pitch_times, is_absolute)	# Go!

	# Make NAO blink its eyes
	def blink(self, eye="both", time=0.3):
		# <eye> = which eye to blink
		# <time> = number of seconds to complete blink
		if eye == "left" or eye == "l":		# If left eye
			t = "top_left"	
			u = "upper_left"
			m = "middle_left"
			l = "lower_left"
			b = "bottom_left"
		elif eye == "right" or eye == "r":	# If right eye
			t = "top_right"
			u = "upper_right"
			m = "middle_right"
			l = "lower_right"
			b = "bottom_right"
		else:								# If both eyes
			t = "top"
			u = "upper"
			m = "middle"
			l = "lower"
			b = "bottom"
		self.leds.off(t)					# Turn off top LEDs
		self.leds.off(b)					# Turn off bottom LEDs
		sleep(time / 5.0)
		self.leds.off(u)					# Turn off upper LEDs
		self.leds.off(l)					# Turn off lower LEDs
		sleep(time / 5.0)
		self.leds.off(m)					# Turn off middle LEDs
		sleep(time / 5.01)
		self.leds.on(m)						# Turn on middle LEDs
		sleep(time / 5.0)
		self.leds.on(u)						# Turn on upper LEDs 
		self.leds.on(l)						# Turn on lower LEDs
		sleep(time / 5.0)
		self.leds.on(t)						# Turn on top LEDs
		self.leds.on(b)						# Turn on bottom LEDs

	# Make NAO wave
	def wave(self, n=2, time=0.6, arm="right", intensity=1):
		# <n> = number of waves
		# <time> = seconds for each wave
		# <arm> = which arm to wave
		# <intensity> = magnitude of the waving motion (0 -> 1)
		if arm == "left" or arm == "l":
			arm_name = "LArm"
			shoulder_pitch = "LShoulderPitch"
			shoulder_roll = "LShoulderRoll"
			elbow_roll = "LElbowRoll"
			elbow_yaw = "LElbowYaw"
			wrist_yaw = "LWristYaw"
			inv = -1
		else:
			arm_name = "RArm"
			shoulder_pitch = "RShoulderPitch"
			shoulder_roll = "RShoulderRoll"
			elbow_roll = "RElbowRoll"
			elbow_yaw = "RElbowYaw"
			wrist_yaw = "RWristYaw"
			inv = 1
		if intensity > 1:
			intensity = 1
		# Joint start angles
		shoulder_pitch_start = -25
		shoulder_roll_start = -10
		elbow_roll_start = 50		
		elbow_yaw_start = 70
		wrist_yaw_start = -85
		# Joint end angles
		shoulder_pitch_end = 85
		shoulder_roll_end = 10.5
		elbow_roll_end = 23.5
		elbow_yaw_end = 68.5
		wrist_yaw_end = -6
		# Joint angles for waving
		shoulder_roll_wave = (30 - intensity * 60.0, 30 + intensity * 60.0)
		elbow_yaw_wave = (90 + intensity * 30.0, 90 - intensity * 30.0)
		# Settings
		is_absolute = True
		self.motion.setStiffnesses(arm_name, 0.5)
		# Raise Arm
		joints = [shoulder_pitch, shoulder_roll, elbow_roll, elbow_yaw, wrist_yaw]
		angle_lists = [[radians(shoulder_pitch_start)],
		[inv * radians(shoulder_roll_start)],
		[inv * radians(elbow_roll_start)],
		[inv * radians(elbow_yaw_start)],
		[inv * radians(wrist_yaw_start)]]
		time_lists = [[1]] * len(angle_lists)
		self.motion.angleInterpolation(joints, angle_lists, time_lists, is_absolute)
		# Wave
		joints = [shoulder_roll, elbow_yaw]
		shoulder_roll_angles = [inv * radians(shoulder_roll_wave[0]), inv * radians(shoulder_roll_wave[1])] * n
		shoulder_roll_intervals = [time / 2.0] * 2 * n
		shoulder_roll_times = intervals2times(shoulder_roll_intervals)
		elbow_yaw_angles = [inv * radians(elbow_yaw_wave[0]), inv * radians(elbow_yaw_wave[1])] * n
		elbow_yaw_intervals = [time / 2.0] * 2 * n
		elbow_yaw_times = intervals2times(elbow_yaw_intervals)
		angle_lists = [shoulder_roll_angles, elbow_yaw_angles]
		time_lists = [shoulder_roll_times, elbow_yaw_times]
		self.motion.angleInterpolation(joints, angle_lists, time_lists, is_absolute)
		# Lower Arm
		joints = [shoulder_pitch, shoulder_roll, elbow_roll, elbow_yaw, wrist_yaw]
		angle_lists = [[radians(shoulder_pitch_end)],
		[inv * radians(shoulder_roll_end)],
		[inv * radians(elbow_roll_end)],
		[inv * radians(elbow_yaw_end)],
		[inv * radians(wrist_yaw_end)]]
		time_lists = [[1]] * len(angle_lists)
		self.motion.angleInterpolation(joints, angle_lists, time_lists, is_absolute)

	# Make NAO face_palm (use with )
	def face_palm(self, arm="right"):
		if arm == "left" or arm == "l":
			arm_name = "LArm"
			shoulder_pitch = "LShoulderPitch"
			shoulder_roll = "LShoulderRoll"
			elbow_roll = "LElbowRoll"
			elbow_yaw = "LElbowYaw"
			wrist_yaw = "LWristYaw"
			hand = "LHand"
			inv = -1
		else:
			arm_name = "RArm"
			shoulder_pitch = "RShoulderPitch"
			shoulder_roll = "RShoulderRoll"
			elbow_roll = "RElbowRoll"
			elbow_yaw = "RElbowYaw"
			wrist_yaw = "RWristYaw"
			hand = "RHand"
			inv = 1
		# Joint start angles
		shoulder_pitch_start = 25
		shoulder_roll_start = 18
		elbow_roll_start = 88.5		
		elbow_yaw_start = 50
		wrist_yaw_start = 62
		hand_start = 0
		# Joint end angles
		shoulder_pitch_end = 85
		shoulder_roll_end = 10.5
		elbow_roll_end = 23.5
		elbow_yaw_end = 68.5
		wrist_yaw_end = -6
		hand_end = 0.46

		is_absolute = True
		self.motion.setStiffnesses(arm_name, 0.9)
		self.motion.setStiffnesses("Head", 0.9)

		# Get head shake lists
		head_joints, head_angles, head_times = \
				self.shake_head(n=4, yaw=20, time=0.5, pitch=25, reset_time=1, exe=False)

		# Raise Arm
		joints = [shoulder_pitch, shoulder_roll, elbow_roll, elbow_yaw, wrist_yaw, hand] + head_joints
		angle_lists = [[radians(shoulder_pitch_start)],
		[inv * radians(shoulder_roll_start)],
		[inv * radians(elbow_roll_start)],
		[inv * radians(elbow_yaw_start)],
		[inv * radians(wrist_yaw_start)],
		[hand_start]] + head_angles
		time_lists = [[1]] * 6 + head_times
		self.motion.angleInterpolation(joints, angle_lists, time_lists, is_absolute)

		# Lower Arm
		joints = [shoulder_pitch, shoulder_roll, elbow_roll, elbow_yaw, wrist_yaw, hand]
		angle_lists = [[radians(shoulder_pitch_end)],
		[inv * radians(shoulder_roll_end)],
		[inv * radians(elbow_roll_end)],
		[inv * radians(elbow_yaw_end)],
		[inv * radians(wrist_yaw_end)],
		[hand_end]]
		time_lists = [[1]] * len(angle_lists)
		self.motion.angleInterpolation(joints, angle_lists, time_lists, is_absolute)

	# Make NAO stomp its feet in a tantrum
	def tantrum(self, n=4):
		# <n> = number of stomps
		pass

	# Flash eyes a given color
	def flash_eyes(self, color="b", n=3, time=0.4):
		if color == "green" or color == "g":
			led_colors = ["red", "blue"]
		elif color == "red" or color =="r":
			led_colors = ["blue", "green"]
		elif color == "turquoise" or color == "t":
			led_colors = ["red"]
		elif color == "pink" or color == "p":
			led_colors = ["green"]
		elif color == "yellow" or color == "y":
			led_colors = ["blue"]
		else:										# Default is blue
			led_colors = ["red", "green"]
		for count in range(n):
			[self.leds.off(color) for color in led_colors]
			sleep(time / 2.0)
			[self.leds.on(color) for color in led_colors]
			sleep(time / 2.0)

	# Turn all ear LEDs on
	def ears_on(self):
		self.leds.on("ears")

	# Turn all ear LEDs off
	def ears_off(self):
		self.leds.off("ears")

	# Make NAO celebrate
	def celebrate(self, arm="right"):
		if arm == "left" or arm == "l":
			arm_name = "LArm"
			shoulder_pitch = "LShoulderPitch"
			shoulder_roll = "LShoulderRoll"
			elbow_roll = "LElbowRoll"
			elbow_yaw = "LElbowYaw"
			wrist_yaw = "LWristYaw"
			hand = "LHand"
			inv = -1
		else:
			arm_name = "RArm"
			shoulder_pitch = "RShoulderPitch"
			shoulder_roll = "RShoulderRoll"
			elbow_roll = "RElbowRoll"
			elbow_yaw = "RElbowYaw"
			wrist_yaw = "RWristYaw"
			hand = "RHand"
			inv = 1
		# Joint angles
		shoulder_pitch_angles = [-17, 32, 3, 32, 32, 85]
		shoulder_roll_angles = [14, 10, 7, 10, 10, 10]
		elbow_roll_angles = [55, 88, 70, 88, 88, 23]	
		elbow_yaw_angles = [95, 88, 88, 88, 88, 68]
		wrist_yaw_angles = [70, 91, 91, 91, 91, -6]
		hand_position = [1, 0, 0, 0, 0, 0.45]

		shoulder_pitch_angles = [radians(i) for i in shoulder_pitch_angles]
		shoulder_roll_angles = [inv * radians(i) for i in shoulder_roll_angles]
		elbow_roll_angles = [inv * radians(i) for i in elbow_roll_angles]
		elbow_yaw_angles = [inv * radians(i) for i in elbow_yaw_angles]
		wrist_yaw_angles = [inv * radians(i) for i in wrist_yaw_angles]

		is_absolute = True
		self.motion.setStiffnesses(arm_name, 1)

		joints = [shoulder_pitch, shoulder_roll, elbow_roll, elbow_yaw, wrist_yaw, hand]
		angle_lists = [shoulder_pitch_angles, 
		shoulder_roll_angles,
		elbow_roll_angles, 
		elbow_yaw_angles,
		wrist_yaw_angles, 
		hand_position]
		time_lists = [[1, 1.5, 2, 2.5, 3.2, 4.2]] * len(joints)
		self.motion.angleInterpolation(joints, angle_lists, time_lists, is_absolute)

	# Demonstrate some example animations
	def demo(self):
		self.wave(arm="l", intensity=0.8)
		self.blink()
		sleep(0.5)
		self.blink()
		sleep(1)
		self.nod_head(n=2, pitch=(-10, 20), time=0.7)
		sleep(1)
		self.blink(eye="left")
		sleep(1)
		self.shake_head(n=4, yaw=20, time=0.5, pitch=25, reset_time=1)
		sleep(1)
		self.shake_head(n=6, yaw=8, time=0.2)
		sleep(1)
		self.face_palm()
		a.ears_off()
		sleep(1)
		a.ears_on()
		sleep(1)
		self.celebrate(arm="r")
		self.flash_eyes()

# Converts a lits of time intervals into a list of times
def intervals2times(intervals):
	n = len(intervals)
	times = [sum(intervals[0:i + 1]) for i in range(n)]
	return times

	
if __name__ == "__main__":
	a = Animations("10.42.0.208", 9559)
