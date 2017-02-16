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

Result = namedtuple('Result', ['path', 'root', 'fingerprint', 'pressure', 'partnumber'])

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

    Returns
    -------
    List of namedtuple of (path, root, fingerprint, pressure, partnumber)
    """
    # root, 7digit fingerprint, maybe a pressure, part number
    pat = '(\w+?)_(\w{7})(?:_P(.+?))?_part(\d+)'
    all_results = (re.match(pat, val) for val in os.listdir('.')
                   if os.path.isdir(val))
    results = [Result(*((m.string,) + m.groups()))
               for m in all_results if (not m is None and m.groups()[0] == root)]
    # Sort results by pressure, then within each pressure the partnumber
    results = sorted(results, key=lambda x: (x.pressure, x.partnumber))

    return results
