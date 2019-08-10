

import math
import time
from matplotlib.pyplot import plot
class Heater():
	# fejk heater to test controller, should be controlling the heater and measure the temperature
	# setHeater and getTemp should be used and replaced
    def __init__(self):

		# parameters for the fejk water pot
        self.water_temp = 10
        self.room_temp = 10
        
        self.liters = 10
        self.heater_power_wanted = 0
        self.heater_power_actual = 0		
        self.k_steel =50
        self.heat_capacity = 4.2
        self.r_inner = 0.2
        self.r_outer = 0.22
        self.l_loss = self.liters/math.pi/self.r_inner/self.r_inner/100
        self.partly_increase = 20.
        		
        		# might not be needed, only for post processing and printing. 
        self.temp_time = []
        self.time = []
        self.time.append(0)
        self.temp_time.append(self.water_temp)
        
        		# based on the heating plate
        self.max_power = 1200
        self.min_power = 0
        self.heater_steps = 200

    def setHeaterPID(self,uk):
        # set heater powers for PID 
        if (uk > self.max_power):
            self.heater_power_wanted = 1200
        else:
            self.heater_power_wanted = uk# 1200/4000*uk

    def setHeater(self,option):
		# set heater powers 
        if option == "up":
            if self.heater_power_wanted < self.max_power:
                self.heater_power_wanted += self.heater_steps

        elif option == "down":
            if self.heater_power_wanted > self.heater_steps:
                self.heater_power_wanted -= self.heater_steps

        elif option == "max":
            self.heater_power_wanted = self.max_power

        elif option == "off":
            self.heater_power_wanted = 0

    def getTemp(self):
		# get temperature of the water
        return self.water_temp

    def step(self):
		# this function should be removed for the real thing 
		#linjär interpolation från temp innan förändring av temp.
        self.water_temp = (((self.heater_power_wanted - self.heater_power_actual)/self.partly_increase +self.heater_power_actual - 2*math.pi*self.k_steel*self.l_loss*(self.water_temp - self.room_temp)/1000/math.log(self.r_outer/self.r_inner))/self.heat_capacity/self.liters/1000 + self.water_temp)
        self.temp_time.append(self.water_temp)
        self.time.append(self.time[-1]+1)
        self.heater_power_actual = (self.heater_power_wanted - self.heater_power_actual)/self.partly_increase +self.heater_power_actual

    def stepTime(self,time):
		# this function should be removed for the real thing
        for t in range(time):
            self.step()


class Controller():
    def __init__(self,timings = [10],temperatures = [60], timestep = 60):
        # create connection to hardward
        self.heater = Heater()
		# define in what intervals the controller should update
        self.timesteps = timestep
        #PID parameters
        self.nTime = 30000
        self.t_d = 10
        self.k_pid = 70

		# the malting scheme
        self.times = [t*60 for t in timings]
        self.temps = temperatures
        self.cook_times = {}

    def run_PID(self): 
        index = 0 
        temp_wanted = self.temps[index]
        temp_actual = self.heater.getTemp()
        nTime = self.nTime 
        t_d = self.t_d
        K=self.k_pid
        #logga temp 
        temp_list=[temp_actual]
        asd = 0 
        ik = 0 
        ek = temp_wanted-temp_actual
        u = []
        while(True): 
            temp_actual = self.heater.getTemp()
            ek_tmp = ek 
            ek = temp_wanted - temp_actual
            ik = ik + ek/nTime
            uk = K*(ek + ik + t_d*(ek-ek_tmp))
            temp_list.append(self.heater.getTemp())
            asd += 1 
            self.heater.setHeaterPID(uk)
            self.heater.step()
            u.append(uk)
            print(str(uk) +"     "+ str(self.heater.getTemp()))
            if abs(temp_actual - temp_wanted) < 1 :
                tmp_temp_list = []
                for i in range(0,self.times[index]):
                    temp_actual = self.heater.getTemp()
                    tmp_temp_list.append(temp_actual)
                    ek_tmp = ek 
                    ek = temp_wanted - temp_actual
                    ik = ik + ek/nTime
                    uk = K*(ek + ik + t_d*(ek-ek_tmp))
                    temp_list.append(self.heater.getTemp())
                    asd += 1 
                    self.heater.setHeaterPID(uk)
                    self.heater.step()
                    u.append(uk)
                    print(str(uk) +"     "+ str(self.heater.getTemp()))
                self.cook_times['index'+str(index)] = tmp_temp_list
                index = index + 1 
                if index > 2 : 
                    print('maltning klar')
                    break
                temp_wanted = self.temps[index]
        plot(u)
        plot(temp_list)

#    def run(self):
#		# create temporary parameters used by the controller
#        index = 0
#        finished = False
#        preheating = False
#        heating = False
#        maxindex = len(self.times) -1
#        previous_temp = 0
#
#		# start the process
#        while not finished:
#			# if heating is requiered, turn on heater to max
#            if not preheating and (self.heater.getTemp() < self.temps[index]):
#                self.heater.setHeater('max')
#
#
#			# heat the water to the requested temperature
#            while (not preheating):
#				# only used for the fejk system
#                self.heater.stepTime(self.timesteps)
#
#				# should be the timesteps (now ms to speed it up)
#                time.sleep(self.timesteps/10000)
#
#				# check if the requiered temperature is 
#                if self.heater.getTemp() >= (self.temps[index]-2):
#                    preheating = True
#                    self.heater.setHeater('off')
#            print("Water is warm after: " + str(self.heater.time[-1]/60) + " min")
#			
#			# set previous temp for controller
#			previous_temp = self.heater.getTemp()
#			# start the timer and keep the wanted temperature
#			for t in range(int(self.times[index]/self.timesteps)):
#				# only used for the fejk system
#				self.heater.stepTime(self.timesteps)
#
#				# should be the timesteps (now ms to speed it up)
#				time.sleep(self.timesteps/10000)
#				
#				print(self.heater.getTemp())
#				# check if heater needs to be turned up, or turned off
#				# conditions, lower temperature, or that the temperature is reducing even though heating is on
#				if ((self.heater.getTemp() < self.temps[index]) and not heating) or ((self.heater.getTemp() < self.temps[index]) and heating and (self.heater.getTemp() < previous_temp)):
#					# try to increas power if possible (should not happen)
#					if self.heater.heater_power_wanted < self.heater.max_power:
#						self.heater.setHeater('up')
#						heating = True
#				else:
#					self.heater.setHeater('off')
#					heating = False
#
#			# continue with the next temperature wanted, or finish everything
#			if index < maxindex:
#				index += 1
#				if self.temps[index-1] < self.temps[index]:
#					preheating = False
#			else:
#				finished = True
#				self.heater.setHeater('off')
#				print("Malting finished!")
#				plot(self.heater.temp_time)


if __name__ == "__main__":
	time_maltingsteps = [30, 400, 90]
	temp_maltingsteps = [60, 70, 80]
	timestep = 10
	c = Controller(time_maltingsteps,temp_maltingsteps,timestep)
	c.run_PID()

