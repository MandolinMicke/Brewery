import sys
import time
import RPi.GPIO as GPIO
import math

# set mode to GPIO
GPIO.setmode(GPIO.BOARD)

DEFAULT_STEP_PINS = [11,13,15,19]

class MotorController():
	def __init__(self,delaytime = 0.001,StepPins = DEFAULT_STEP_PINS):
		self.time_delay = delaytime
		self.step_pins = StepPins
		for pin in self.step_pins :
		  print("Setting up pins..")
		  GPIO.setup(pin,GPIO.OUT)
		  GPIO.output(pin, False)
		  
		self.sequences = [[1,0,0,1],
       	[1,0,0,0],
       	[1,1,0,0],
       	[0,1,0,0],
       	[0,1,1,0],
       	[0,0,1,0],
       	[0,0,1,1],
       	[0,0,0,1]]

		self.step_count = len(self.sequences)
		self.step_dir = 1 # positive or negative
		self.step_amount = 1 # one or two
		self.counter = 0
		self.position = 0
		
	def resetPosition(self):
		self.position = 0
		
	def changeDirection(self,direction = None):
		if direction == None:
			if self.step_dir == 1:
				self.step_dir = -1
			else:
				self.step_dir = 1
		else:
			self.step_dir = direction
		
	def getNextSequence(self):
		self.counter += self.step_dir*self.step_amount
		if (self.counter >= self.step_count):
			self.counter = self.counter%self.step_count
		if (self.counter < 0):
			self.counter += self.step_count
		return self.sequences[self.counter]
		
	def step(self,new_seq = None):
		if new_seq == None:
			new_seq = self.getNextSequence()
#		print(new_seq)
		for pin in range(0, 4):
			xpin = self.step_pins [pin]#
			if new_seq[pin]!=0:
			  GPIO.output(xpin, True)
			else:
			  GPIO.output(xpin, False)
			time.sleep(self.time_delay )
	
	def turnOff(self):
		self.step([0,0,0,0])
	
	def turnDegrees(self,deg):
		if deg < 0:
			self.step_dir = -1
		else:
			self.step_dir = 1
		
		fullrev = 1024*4/self.step_amount
		numsteps = math.ceil(fullrev*deg/360)
		for i in range(numsteps):
			self.step()
		self.turnOff()
		
	def turnToPosition(self,pos):
		diffpos = pos - self.position

		if diffpos < 0:
			self.step_dir = -1
			diffpos = -diffpos
		else:
			self.step_dir = 1
		
		fullrev = 1024*4/self.step_amount
		numsteps = math.ceil(fullrev*diffpos)

		for i in range(numsteps):
			self.step()
		self.turnOff()
		self.position = pos
		
if __name__ == '__main__':
	mc = MotorController(0.001)
	mc.turnOff()
	mc.step_amount = 1
	mc.turnToPosition(0.2)
	time.sleep(1)
	mc.turnToPosition(0.1)
	time.sleep(1)
	mc.turnToPosition(0.3)
	time.sleep(1)
	mc.turnToPosition(0)
	
	
	
	
	
		
		
		
		
		
		
		
