#!/usr/bin/env python2
'''
this script reads and plots data from an arduino through serial port
Usage:
    read_analog_data <device> <baud> [options]

Options:
    --buffer=<N>     How many entries to buffer before replotting [default: 20]
    --storage=<N>    How many entries to store in total [default: 1000]
    --interval=<N>   Update interval for the plot in milliseconds, [default: 10]
    --out=<file>     Outputfile
    --skiplines=<N>  how many lines to skip before starting plot [default: 100]
'''
from __future__ import division, print_function
from matplotlib.style import use

use('dark_background')
use('matplotlibrc')

import matplotlib.pyplot as plt
import matplotlib.animation as ani
import serial
from docopt import docopt
from adcvalues_pb2 import SerialData
from ringbuffer import Buffer
import numpy as np


def init_plot():
    fig, ax = plt.subplots()
    ax.autoscale(False)

    adc_curve, = ax.plot([], [], '-', label='A0')
    ax.set_ylim(-50, 1100)
    ax.set_yticks([0, 256, 512, 768, 1024])
    ax.set_ylabel(r'adc value')
    ax.set_xlabel('$t$ / s')
    ax.legend(bbox_to_anchor=(0.5, 1.02), loc='center')
    ax.grid()
    fig.tight_layout()

    return fig, ax, adc_curve


def updatefig(x):
    for i in range(buffer_size):
        read(output)
    mask = ~np.isnan(ts.data)
    adc_curve.set_data(ts.data[mask], signal.data[mask])
    if len(ts) > 2:
        lower = ts[mask][0]
        upper = ts[mask][-1]
        ax.set_xlim(lower, upper + 0.1 * (upper - lower))

    return adc_curve


def read(output=None):
    global ts, signal
    data = SerialData()
    try:
        line = arduino.readline().rstrip()
    except:
        print('could not readline from arduino')
    try:
        data.ParseFromString(line)
        t = data.time / 1000
        adcvalue = data.adcvalue

        signal.fill(adcvalue)
        ts.fill(t)

        if output is not None:
            output.write("{:1.3f},{:d}\n".format(t, adcvalue))

    except Exception as e:
        print(e)

if __name__ == '__main__':
    args = docopt(__doc__)

    buffer_size = int(args['--buffer'])
    storage_size = int(args['--storage'])
    interval = int(args['--interval'])
    num_skip = int(args['--skiplines'])

    try:
        arduino = serial.Serial(args['<device>'], args['<baud>'])
    except Exception as e:
        raise IOError('connection to arduino failed with error: \n\n', e)

    # read the first lines to get rid of junk before restart
    for i in range(num_skip):
        _ = arduino.readline(20)

    fig, ax, adc_curve = init_plot()
    ts = Buffer(storage_size)
    signal = Buffer(storage_size)

    if args['--out'] is not None:
        output = open(args['--out'], 'w')
        output.write('t,ADC0\n')
    else:
        output = None

    try:
        ani = ani.FuncAnimation(fig, updatefig, interval=interval)
        plt.show()
    except KeyboardInterrupt:
        if output is not None:
            output.close()
