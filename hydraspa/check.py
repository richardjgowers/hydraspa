from __future__ import print_function

import glob

from .util import STATUSES, is_finished


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


