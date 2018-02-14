"""Common functions for this stuff

"""
from collections import namedtuple
import glob
import re
import os


STATUSES = {
    0: 'FINISHED',
    1: 'IN PROGRESS',
    2: 'NOT STARTED',
}

Result = namedtuple('Result', ['temperature', 'pressure', 'partnumber', 'path'])

def is_finished(dirname):
    """Check if raspa simulation in *dirname* finished"""
    # fn of output file
    try:
        output = glob.glob(os.path.join(dirname, 'Output', 'System_0', '*.data'))[0]
    except IndexError:  # output not created, sim not started
        return 2
    with open(output, 'rb') as f:
        f.seek(-100, 2)  # seek to 100 bytes before EOF
        done = b'Simulation finished' in f.read()
    if done:
        return 0
    else:
        return 1


def conv_to_number(val, conv):
    """Convert a string to a number

    Can apply either a k (thousand) or M (million) multiplier

    Parameter
    ---------
    val : str
      String representing the number
    conv
      Function to apply to final number, float/int

    Example
    -------
    ('100k', int) -> 100,000
    ('5.6M', float) -> 5,600,000.0

    """
    if val[-1].isalpha():
        val, suffix = val[:-1], val[-1]
        try:
            multi = {'k': 1e3, 'M':1e6}[suffix]
        except KeyError:
            raise ValueError("Unrecognised suffix {}".format(suffix))
    else:
        multi = 1

    # apply float first, so ('5.4k', int) -> int(float(5.4) * 1000)
    return conv(float(val) * multi)


def discover(root):
    """Find all children of *root*

    Parameters
    ----------
    root : str
      path to directory to search

    Returns
    -------
    Sorted list of namedtuple of (path, temperature, pressure, partnumber)
    """
    pat = r'T(\d+\.\d+)_P(\d+\.\d+)_part(\d+)'

    children = []
    for dirname in os.listdir(root):
        mat = re.match(pat, dirname)

        if mat is not None:
            T, P, part = mat.groups()
            T, P, part = float(T), float(P), int(part)
            children.append(Result(T, P, part, os.path.join(root, dirname)))

    return sorted(children,
                  key=lambda x: (x.temperature, x.pressure, x.partnumber))
