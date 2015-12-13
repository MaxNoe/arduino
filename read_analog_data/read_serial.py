#!/usr/bin/env python2
'''
this script reads and plots data from an arduino through serial port
Usage:
    read_analog_data <device> <baud> [options]

Options:
    --buffer=<N>     How many entries to buffer before replotting [default: 50]
    --storage=<N>    How many entries to store in total [default: 5000]
    --interval=<N>   Update interval for the plot in milliseconds, [default: 20]
    --out=<file>     Outputfile
    --skiplines=<N>  how many lines to skip before starting plot [default: 200]
    --channels=<C>   Which channels to plot, comma separated [default: 0]
    --every=<N>      Plot only every Nth point [default: 1]
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

csv_row = "{t:1.3f},{data.adc0:d},{data.adc1:d},{data.adc2:d},{data.adc3:d}\n"


def init_plot():
    fig, ax = plt.subplots()
    ax.autoscale(False)

    lines = {}
    for c in channels:
        lines[c], = ax.plot([], [], '-', label=str(c))
    ax.set_ylim(-50, 1100)
    ax.set_yticks([0, 256, 512, 768, 1024])
    ax.set_ylabel(r'adc value')
    ax.set_xlabel('$t$ / s')
    ax.legend(loc='upper center', ncol=4)
    ax.grid()
    fig.tight_layout()

    return fig, ax, lines


def updatefig(x):
    for i in range(buffer_size):
        read(output)

    mask = ~np.isnan(ts.data)
    for c in channels:
        lines[c].set_data(
            ts.data[mask][::plotstep],
            signal[c].data[mask][::plotstep],
        )

    if len(ts) > 2:
        lower = ts[mask][0]
        upper = ts[mask][-1]
        ax.set_xlim(lower, upper + 0.1 * (upper - lower))

    return lines


def read(output=None):
    global ts, signal
    data = SerialData()
    success = False
    while not success:
        try:
            line = arduino.readline().rstrip()
        except:
            print('could not readline from arduino')
        try:
            data.ParseFromString(line)
            success = True
        except Exception:
            line = arduino.readline()
    else:
        t = data.time / 1000
        if t == 0:
            return

        for c in channels:
            signal[c].fill(getattr(data, 'adc{}'.format(c)))
        ts.fill(t)

        if output is not None:
            output.write(csv_row.format(t=t, data=data))


if __name__ == '__main__':
    args = docopt(__doc__)

    buffer_size = int(args['--buffer'])
    storage_size = int(args['--storage'])
    interval = int(args['--interval'])
    num_skip = int(args['--skiplines'])

    channels = [int(c) for c in args['--channels'].split(',')]
    plotstep = int(args['--every'])

    try:
        arduino = serial.Serial(args['<device>'], args['<baud>'], timeout=0.005)
    except Exception as e:
        raise IOError('connection to arduino failed with error: \n\n', e)

    # read the first lines to get rid of junk before restart
    for i in range(num_skip):
        _ = arduino.readline(20)

    fig, ax, lines = init_plot()
    ts = Buffer(storage_size)
    signal = {c: Buffer(storage_size) for c in channels}

    if args['--out'] is not None:
        output = open(args['--out'], 'w')
        output.write('t,adc0,adc1,adc2,adc3\n')
    else:
        output = None

    try:
        ani = ani.FuncAnimation(fig, updatefig, interval=interval)
        plt.show()
    except KeyboardInterrupt:
        if output is not None:
            output.close()
