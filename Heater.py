from temp import DS18B20
from MotorController import MotorController

class Heater():


	def __init__(self,maxpower = 2000):
		self.Temp = DS18B20()
		c = self.Temp.device_count()
		if c < 1:
			raise OSError('Could not find temperature sensor')
		self.mc = MotorController()
		self.mc.step_amount = 1
		self.maxpower = 2000
		self.maxturning = 0.9
	def getTemp(self):
		return self.Temp.tempC(0)
		
	def setHeaterPID(self,uk):
		wanted_movement = uk/self.maxpower
		if wanted_movement > self.maxturning:
			self.mc.turnToPosition(self.maxturning)
		elif (wanted_movement < 0):
			self.mc.turnToPosition(0)
		else:
			self.mc.turnToPosition(wanted_movement)

if __name__ == '__main__':
	h = Heater()
	print(h.getTemp())
