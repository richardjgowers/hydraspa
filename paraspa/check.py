from __future__ import print_function

import glob
import os

STATUSES = {
    0: 'FINISHED',
    1: 'IN PROGRESS',
    2: 'NOT STARTED',
}

def check(dirname):
    """Check the progress of tasks starting with *dirname*"""
    children = glob.glob('{}_part_*'.format(dirname))
    # order children
    def childno(name):
        return int(name.split('_')[-1])
    children = sorted(children, key=childno)

    alldone = True

    print("Found {} children".format(len(children)))
    for child in children:
        status = is_finished(child)
        print(" - {} is {}".format(child, STATUSES[status]))
        alldone = alldone and (status == 0)
    if alldone:
        print("All simulations finished!")


def is_finished(dirname):
    """Check if raspa simulation in *dirname* finished"""
    # fn of output file
    try:
        output = glob.glob(os.path.join(dirname, 'Output', 'System_0', '*.data'))[0]
    except IndexError:  # output not created, sim not started
        return 2
    with open(output, 'r') as f:
        f.seek(-100, 2)  # seek to 100 bytes before EOF
        done = 'Simulation finished' in f.read()
    if done:
        return 0
    else:
        return 1
