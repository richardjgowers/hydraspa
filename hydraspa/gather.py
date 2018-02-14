import glob
import os
import numpy as np
import re
import pandas as pd

from .util import discover, is_finished

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
    children = discover(dirname)

    output = {}

    for child in children:
        if is_finished(child.path) == 2:  # skip unfinished directories
            continue
        output[child] = parse_results(child.path).mean()

    return output


# Regex patterns to grab stuff from Raspa output
# grabs the integer values before and after 'out of'
# eg '20 out of 200' -> (20, 200)
CYCLE_PAT = re.compile(r'^[C].+?(\d+)(?: out of )(\d+)')
# matches the instantaneous mol/kg on this line:              vvvvvvvvvvvv
# absolute adsorption:   0.00000 (avg.   0.00000) [mol/uc],   0.0000000000 (avg.   0.0000000000) [mol/kg],   0.0000000000 (avg.   0.0000000000) [mg/g]
MMOL_PAT = re.compile(r'(?:\s+absolute adsorption:).+?(\d+\.\d+)(?=\s+\(avg\.\s+\d+\.\d+\)\s+\[mol\/kg\])')

def parse_results(path):
    """Parse results from a Raspa simulation, returns absolute mol/kg

    Ignores all values from [Init] period. Simulations shouldn't be using
    this option anyway, as we're dealing with equilibration ourselves.

    Parameters
    ----------
    path : str
      path where the simulation took place

    Returns
    -------
    results : pandas.Series
      absolute loadings in mol/kg
    """
    # return pandas series of the results
    outfile = glob.glob(os.path.join(path, 'Output/System_0/*.data'))[0]

    cycles = []
    values = []

    with open(outfile, 'r') as inf:
        for line in inf:
            cmat = re.search(CYCLE_PAT, line)
            if cmat:
                cycles.append(cmat.groups()[0])
                continue
            lmat = re.search(MMOL_PAT, line)
            if lmat:
                values.append(lmat.groups()[0])

    cycles = np.array(cycles, dtype=np.int)
    values = np.array(values, dtype=np.float32)

    df = pd.Series(values, index=cycles)
    df.name = 'density'
    df.index.name = 'time'

    return df
