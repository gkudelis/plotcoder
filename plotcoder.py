import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np
import subprocess, os, sys
import math as M


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

data = sys.stdin.readline().rstrip(' \n')
slide_total = int(data)
# The +1 helps when we have exactly 10^n slides
num_digits = M.ceil(M.log10(slide_total+1))
filename_strf = '%0'+str(num_digits)+'u'
print('Looking forward to '+str(slide_total)+' slides.')

# Read data from stdin and plot at the same time
slide_number = 1
while slide_number <= slide_total:
    line = sys.stdin.readline().rstrip(' \n')
    if len(line) == 0:
        print('Unexpected empty line in input.')
        sys.exit()

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
    fname = 'plot_' + str(filename_strf % slide_number) + '.png'
    plt.savefig(fname, dpi=100)
    print('Writing file ' + fname)

    slide_number += 1

# Make avi and get rid of png's
out_name = dirname + '.avi'
subprocess.check_call(['mencoder', 'mf://*.png', '-mf', 'fps=25',
    '-o', out_name, '-ovc', 'lavc', '-lavcopts', 'vcodec=mpeg4'])

for fname in os.listdir(wdir):
    if fname == out_name:
        continue
    print('Removing: ' + fname)
    os.remove(os.path.join(wdir, fname))
