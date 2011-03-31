import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np
import subprocess, os, sys


if (len(sys.argv) < 2):
    print('Usage: python plotcoder.py DEST_DIR')
    sys.exit()

dirname = sys.argv[1]
try:
    cwd = os.getcwd()
    wdir = os.path.join(cwd, dirname)
    os.mkdir(wdir)
    os.chdir(wdir)

except OSError:
    print('Directory already exists.')
    sys.exit()

slide_number = 0;

# Read data from stdin and plot at the same time
while True:
    slide_number += 1

    line = sys.stdin.readline().rstrip(' \n')
    if len(line) == 0:
        break

    data = line.split(' ')
    time = float(data[0])

    # Parse position data
    pos_data = []
    for i in range(1,len(data),2):
        pos_data.append({
            'x': float(data[i]),
            'y': float(data[i+1]),
        })

    # Init plotting
    plt.clf()
    plt.axis((-100,100,-100,100))
    
    # Plot points
    for point in pos_data:
        plt.plot(point['x'], point['y'], 'b.')

    # Save to image file
    fname = 'plot_' + str('%03u' % slide_number) + '.png'
    plt.savefig(fname, dpi=100)
    print('Writing file ' + fname)

# Make avi and get rid of png's
out_name = dirname + '.avi'
subprocess.check_call(['mencoder', 'mf://*.png', '-mf', 'fps=25',
    '-o', out_name, '-ovc', 'lavc', '-lavcopts', 'vcodec=mpeg4'])

for fname in os.listdir(wdir):
    if fname == out_name:
        continue
    print('Removing: ' + fname)
    os.remove(os.path.join(wdir, fname))
