import matplotlib.pyplot as plt
import matplotlib.animation as ani
import serial
import numpy as np
import time
import sys

try:
    arduino = serial.Serial('/dev/ttyACM0', 19200)
except:
    print("connection to arduino not possible")
    sys.exit(1)
time.sleep(1)

fig, ax = plt.subplots()
ax.autoscale(False)

voltage_curve, = ax.plot([],[], 'r-', label="Spannung")
ax.set_ylim(0, 5.1)
ax.set_ylabel(r"$U$/V")

ts = []
signal = []

def do_step():
    global ts, signal
    try:
        line = arduino.readline()
    except:
        print("could not readline from ardiuno")
    try:
        t, voltage = line.decode().split(",")
        voltage = float(voltage)
        t = round(float(t)/1000,1)
        if len(signal)<1000:
            signal.append(voltage)
            ts.append(t)
        else:
            signal = signal[1:]
            signal.append(voltage)
            ts = ts[1:]
            ts.append(t)
    except:
        print("skipped invalid value")

def updatefig(x):
    for i in range(20):
        do_step()
    voltage_curve.set_data(ts, signal)
    ax.set_xlim(max(0, ts[0]), ts[-1]+0.5)

ani = ani.FuncAnimation(fig, updatefig, interval=10)
plt.show()
