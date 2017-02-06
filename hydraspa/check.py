from __future__ import print_function

import glob
import re

from .util import DIR_PATTERN, STATUSES, is_finished

# regex match for '52' in 'mysim_part52'
PART_PATTERN = re.compile('.+?part(\w+)')


def check(dirname):
    """Check the progress of tasks starting with *dirname*"""
    children = glob.glob(DIR_PATTERN.format(root=dirname))
    # order children
    def childno(name):
        return int(re.match(PART_PATTERN, name).group(1))
    children = sorted(children, key=childno)

    alldone = True

    print("Found {} children".format(len(children)))
    for child in children:
        status = is_finished(child)
        print(" - {} is {}".format(child, STATUSES[status]))
        alldone = alldone and (status == 0)
    if alldone:
        print("All simulations finished!")


