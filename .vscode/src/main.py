import serial.tools.list_ports
import numpy as np
import matplotlib.pyplot as plt
import datetime
import csv

from matplotlib.animation import FuncAnimation
from scipy.interpolate import make_interp_spline

#globals
portsList = []
pressureData = []
forceData = []
graphTime = []


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

dataPort = serial.Serial(want, 115200) #initializing and opening the serial port

#setting up our CSV for storage
f = ["Pressure", "Force", "Time"]
with open('data.csv', 'w') as file:
    writer = csv.DictWriter(file, fieldnames=f)
    writer.writeheader()


#function for parsing data
def parseGraphData(toParse):
    info = str(toParse).split(",")
    pressureVal = info[0].split(":")[1]
    index = info[1].split(":")[1].find("\\r")
    forceVal = (info[1].split(":")[1])[:index]
    return float(pressureVal), float(forceVal)





#some final initialization
fig, (ax1, ax2) = plt.subplots(2,1)
command = input("Enter command LAUNCH: ")
dataPort.write(command.encode('utf-8'))
startTime = datetime.datetime.now()
endTime = startTime + datetime.timedelta(seconds=10) #initialize a timer
plt.style.use('fivethirtyeight')


def animation(i):
    
    #read in our data and throw it into matplotlib
    if dataPort.in_waiting == 0:
        pass
    data = dataPort.readline()     
    pressure, force = parseGraphData(data)
    pressureData.append(pressure) #the data we want from mcu
    forceData.append(force)
    currTime=(datetime.datetime.now() - startTime).total_seconds() -1 #idk why this -1 is needed but it is
    graphTime.append(currTime)
    
    #store it
    with open('data.csv', 'a') as file:
        writer = csv.DictWriter(file, fieldnames=f)
        info = {
            f[0]:pressure,
            f[1]:force,
            f[2]:currTime
        }
        writer.writerow(info)
    
    #graph it
    ax1.cla()
    ax2.cla()
    ax1.set_title("Pressure and Force over time")
    ax1.set_ylabel("Pressure (kPa)")
    ax2.set_ylabel("Force (N)")
    ax2.set_xlabel("Time (s)")
    ax1.plot(graphTime, pressureData)
    ax2.plot(graphTime, forceData)
    plt.tight_layout()

    #check if we have reached the end of the timer
    # currT = datetime.datetime.now()
    # if currT>endTime:
    #     command = "exit"
    #     dataPort.write(command.encode("utf-8"))



ani = FuncAnimation(plt.gcf(), animation, interval=100)
plt.show()


