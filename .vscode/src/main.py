import serial.tools.list_ports
import numpy as np
import matplotlib.pyplot as plt
import datetime
import csv

from functools import partial
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button
from scipy.interpolate import make_interp_spline

#globals
portsList = []
pressureData = []
forceData = []
timeData = []
receive = False;

#setting up our serial communications
ports = serial.tools.list_ports.comports()


for port in ports:
    portsList.append(str(port))
    print(str(port))
com = input("Select Com: ")
for i in range(len(portsList)):
    if ("COM" + str(com)) in portsList[i]:
        want = "COM" + str(com)
        print(want)

dataPort = serial.Serial(want, 9600, timeout = 3) #initializing and op  ening the serial port

#setting up our CSV for storage 
f = ["Time", "Force", "Pressure"]
with open('data.csv', 'w') as file:
    writer = csv.DictWriter(file, fieldnames=f)
    writer.writeheader()


#function for parsing data
def parseGraphData(toParse):
    try:
        i = str(toParse).find("'")
        info = str(toParse)[i+1:].split(',')
        time = info[0]
        force = info[1]
        i = info[2].find("\\r")
        pressure= info[2][:i]
        return float(time), float(force), float(pressure)
    except Exception as e:
        return 0, 0, 0




#ping button
def ping(i):
    command = "PING"
    dataPort.write(command.encode('utf-8'))
    print("pinged")
    data = dataPort.readline()
    print(data)
    
def launch(i):
    receive = True;
    command = "FIRE"
    dataPort.write(command.encode('utf-8'))
    
    

#some final initialization
fig, (ax1, ax2) = plt.subplots(2,1)
ax1.plot(timeData, pressureData)
ax2.plot(timeData, forceData)
ax1.set_title("Pressure and Force over time")
ax1.set_ylabel("Pressure (psi)")
ax2.set_ylabel("Force (lbs)")
ax2.set_xlabel("Time (μs)")
# command = input("LAUNCH ")
# dataPort.write(command.encode('utf-8'))
startTime = datetime.datetime.now()
endTime = startTime + datetime.timedelta(seconds=10) #initialize a timer
plt.style.use('fivethirtyeight')
#main animation loop
def animation(i):
    
    #graph it
    ax1.cla()
    ax2.cla()
    ax1.set_title("Pressure and Force over time")
    ax1.set_ylabel("Pressure (psi)")
    ax2.set_ylabel("Force (lbs)")
    ax2.set_xlabel("Time (μs)")
    ax1.plot(timeData, pressureData)
    ax2.plot(timeData, forceData)
    plt.tight_layout()
    
    # print("here1")
    #read in our data and throw it into matplotlib
    # if dataPort.in_waiting == 0:
    #     pass
    
        
    # print("here2")
    try:
        if (dataPort.in_waiting != 0):
            data = dataPort.readline() 
            time, force, pressure = parseGraphData(data)
            pressureData.append(pressure) #the data we want from mcu
            forceData.append(force)
            timeData.append(time) 
            #store it
            with open('data.csv', 'a') as file:
                writer = csv.DictWriter(file, fieldnames=f)
                info = {
                    f[0]:time,
                    f[1]:force,
                    f[2]:pressure
                }
                writer.writerow(info) 
        
          
    except serial.SerialException as e:
        print(e)
        
    # print("here3")

    
    
    
    

    #check if we have reached the end of the timer
    # currT = datetime.datetime.now()
    # if currT>endTime:
    #     command = "exit"
    #     dataPort.write(command.encode("utf-8"))




ani = FuncAnimation(plt.gcf(), partial(animation), interval=100)
axping = fig.add_axes([0.7, 0.01, 0.1, 0.075])
axfire = fig.add_axes([0.81, 0.01, 0.1, 0.075])
pingButton = Button(axping, "PING")
pingButton.on_clicked(ping) 
launchButton = Button(axfire, "FIRE")
launchButton.on_clicked(launch)
plt.show()

