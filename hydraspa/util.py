"""Common functions for this stuff

"""
import glob
import os


STATUSES = {
    0: 'FINISHED',
    1: 'IN PROGRESS',
    2: 'NOT STARTED',
}

DIR_PATTERN = "{root}*_part*"

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
