from __future__ import print_function

import glob
import re

from .util import discover, STATUSES, is_finished


def check(dirname):
    """Check the progress of tasks starting with *dirname*"""
    children = discover(dirname)
    children = sorted(children, key=lambda x: (x.pressure, x.partnumber))

    alldone = True

    print("Found {} children".format(len(children)))
    for child in children:
        status = is_finished(child.path)
        print(" - {} is {}".format(child.path, STATUSES[status]))
        alldone = alldone and (status == 0)
    if alldone:
        print("All simulations finished!")


