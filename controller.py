

import math
import time
from matplotlib.pyplot import plot

from Heater import Heater

import logging

logging.basicConfig(level = logging.DEBUG, filename = "temperature.log")

class Controller():
    def __init__(self,timings = [10],temperatures = [60], timestep = 60):
        # create connection to hardward
        self.heater = Heater()
	# define in what intervals the controller should update
        self.timesteps = timestep
	
        #PID parameters
        self.nTime = 100000000000000000
        self.t_d = 10
        self.k_pid = 1000
	
		# the malting scheme
        self.times = [t*60 for t in timings]
        self.temps = temperatures
        self.cook_times = {}

    def run_PID(self): 
        print('maltning börjar')
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
            tempvec = []
            for t in range(0,self.timesteps):
                tempvec.append(self.heater.getTemp())
                time.sleep(1)
            temp_actual = sum(tempvec)/len(tempvec)
            ek_tmp = ek 
            ek = temp_wanted - temp_actual
            ik = ik + ek/nTime
            uk = K*(ek + ik + t_d*(ek-ek_tmp))
            temp_list.append(self.heater.getTemp())
            asd += 1 
            self.heater.setHeaterPID(uk)
            u.append(uk)
#            print(str(uk) +"     "+ str(temp_actual) + "/" + str(temp_wanted))
            logging.debug(" " + str(uk) + " " + str(temp_actual) + " " + str(temp_wanted))
            if abs(temp_actual - temp_wanted) < 1 :
                tmp_temp_list = []
                for i in range(0,self.times[index]):
                    tempvec = []
                    for t in range(0,self.timesteps):
                        tempvec.append(self.heater.getTemp())
                        time.sleep(1)

                    temp_actual = sum(tempvec)/len(tempvec)
                    
                    tmp_temp_list.append(temp_actual)
                    ek_tmp = ek 
                    ek = temp_wanted - temp_actual
                    ik = ik + ek/nTime
                    uk = K*(ek + ik + t_d*(ek-ek_tmp))
                    temp_list.append(self.heater.getTemp())
                    asd += 1 
                    self.heater.setHeaterPID(uk)
                    u.append(uk)
 #                   print(str(uk) +"     "+ str(self.heater.getTemp()) + "/" + str(temp_wanted))
                    logging.debug(" " + str(uk) + " " + str(temp_actual) + " " + str(temp_wanted))
                self.cook_times['index'+str(index)] = tmp_temp_list
                index = index + 1 
                if index > 2 : 
                    print('maltning klar')
                    break
                temp_wanted = self.temps[index]
        plot(u)
        plot(temp_list)

if __name__ == "__main__":
	time_maltingsteps = [10, 10]
	temp_maltingsteps = [70, 80]
	timestep = 10
	c = Controller(time_maltingsteps,temp_maltingsteps,timestep)
	c.run_PID()

