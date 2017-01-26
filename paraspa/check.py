from __future__ import print_function

import glob


def check(dirname):
    """Check the progress of tasks starting with *dirname*"""
    children = glob.glob('{}_part_*'.format(dirname))

    alldone = True

    print("Found {} children".format(len(children)))
    for child in children:
        finished = True
        print(" - {} is {}".format(child, 'FINISHED'))
        alldone = alldone and finished
    if alldone:
        print("All simulations finished!")

