#!/usr/bin/env python3
'''
this script reads and plots data from an arduino through serial port
Usage:
    read_analog_data <device> <baud> [options]

Options:
    --buffer=<N>     How many entries to buffer before replotting [default: 20]
    --storage=<N>    How many entries to store in total [default: 1000]
    --interval=<N>   Update interval for the plot in milliseconds, [default: 5]
'''

from matplotlib.style import use

use('dark_background')
use('matplotlibrc')

import matplotlib.pyplot as plt
import matplotlib.animation as ani
import serial
import numpy as np
import time
from docopt import docopt


args = docopt(__doc__)

buffer_size = int(args['--buffer'])
storage_size = int(args['--storage'])
interval = int(args['--interval'])

try:
    arduino = serial.Serial(args['<device>'], args['<baud>'])
except Exception as e:
    raise IOError('connection to arduino failed with error: \n\n', e)

time.sleep(1)

fig, ax = plt.subplots()
ax.autoscale(False)

voltage_curve, = ax.plot([],[], '-', label='A0')
ax.set_ylim(-50, 1100)
ax.set_yticks([0, 256, 512, 768, 1024])
ax.set_ylabel(r'adc value')
ax.set_xlabel('$t$ / s')
ax.legend(bbox_to_anchor=(0.5, 1.02), loc='center')
ax.grid()
fig.tight_layout()

ts = []
signal = []

def read():
    global ts, signal
    try:
        line = arduino.readline()
    except:
        print('could not readline from arduino')
    try:
        t, voltage = line.decode().split(',')
        voltage = float(voltage)
        t = float(t)/1000
        if len(signal) < storage_size:
            signal.append(voltage)
            ts.append(t)
        else:
            signal[:-1] = signal[1:]
            signal[-1] = voltage
            ts[:-1] = ts[1:]
            ts[-1] = t
    except:
        print('skipped invalid value')

def updatefig(x):
    for i in range(buffer_size):
        read()
    voltage_curve.set_data(ts, signal)
    if len(ts)>2:
        ax.set_xlim(max(0, ts[0]), ts[-1]+0.5)

ani = ani.FuncAnimation(fig, updatefig, interval=interval)
plt.show()
