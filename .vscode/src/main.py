import serial.tools.list_ports
import numpy as np
import matplotlib.pyplot as plt
import datetime

from matplotlib.animation import FuncAnimation
from scipy.interpolate import make_interp_spline

#globals
portsList = []
graphData = []
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



#function for parsing data
def parseGraphData(toParse):
    info = str(toParse).split(",")
    index = info[1].split(":")[1].find("\\r")
    garbageVal = (info[1].split(":")[1])[:index]
    return float(garbageVal)





#some final initialization
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
    print(data) #for debug
    garbage = parseGraphData(data)
    graphData.append(garbage) #the data we want from mcu
    currTime=(datetime.datetime.now() - startTime).total_seconds()
    #print(currTime) #for debug
    graphTime.append(currTime)
    
    #xySpline = make_interp_spline(graphTime, graphData)
    
    #x = np.linspace(graphTime.min(), graphTime.max(), 500)
    #y = xySpline(x)
    
    plt.cla()
    plt.plot(graphTime, graphData)
    plt.title("Garbage over time")
    plt.xlabel("time")
    plt.ylabel("garbo")
    plt.tight_layout()

    #check if we have reached the end of the timer
    # currT = datetime.datetime.now()
    # if currT>endTime:
    #     command = "exit"
    #     dataPort.write(command.encode("utf-8"))



ani = FuncAnimation(plt.gcf(), animation, interval=100)
plt.show()


