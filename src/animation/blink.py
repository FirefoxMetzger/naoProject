from animations import Animations
	
class Blink(Animations):
	def __init__(self,ip,port=9559):
		Animations.__init__(self,ip,port)

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
