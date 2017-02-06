import glob
import os
import numpy as np

from .util import DIR_PATTERN, is_finished

def gather(dirname):
    """Gather the results from all dirs starting with dirname

    Parameters
    ----------
    dirname : str
       root directory name for children

    Returns
    -------
    dict of childname: np array of results
    """
    children = glob.glob(DIR_PATTERN.format(root=dirname))

    output = {}

    for child in children:
        if is_finished(child) == 2:  # skip unfinished directories
            continue
        output[child] = parse_output(child)

    return output


def parse_output(dirname):
    """Returns np array of instantaneous mol/uc values"""
    def _getval1(l):
        # production cycles
        return float(l.split('adsorption:')[1].split('(avg.')[0])
    def _getval2(l):
        # init cycles
        return float(l.split('adsorption:')[1].split('[mol')[0])

    output = glob.glob(os.path.join(dirname, 'Output', 'System_0', '*.data'))[0]

    vals = []
    with open(output, 'r') as f:
        for line in f:
            if line.lstrip(' \t').startswith('absolute adsorption'):
                if 'avg.' in line:
                    vals.append(_getval1(line.lstrip()))
                else:
                    vals.append(_getval2(line.lstrip()))
    return np.array(vals)
