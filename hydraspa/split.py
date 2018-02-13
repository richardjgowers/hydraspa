"""Splits a single simulation dir into many

"""
from __future__ import division

import itertools
from functools import partial
import os
import shutil


def static_pressure(line, amount):
    return 'ExternalPressure {}\n'.format(amount)


def static_temperature(line, amount):
    return 'ExternalTemperature {}\n'.format(amount)


def static_cycles(line, amount):
    return 'NumberOfCycles {}\n'.format(amount)


def zero_init(line):
    # whatever it was, it's zero now
    return 'NumberOfInitializationCycles 0\n'


def split(src, fingerprint, temperatures, pressures, ntasks, ncycles):
    """Split simulation in src into various conditions

    Parameters
    ----------
    src : string
      Name of the directory we wish to copy
    fingerprint : string
      Unique identifier for this setup
    temperatures : list
      List of temperatures (in K) to create
    pressures : list
      Specify a list of pressures (in kPa) to create
    ntasks : int
      Number of copies of *src* to make
    ncycles : int
      Manually set the number of cycles per simulation.
    """
    src = src.strip('/')

    if not os.path.exists(src):
        raise ValueError("Template not found")

    newdirs = []

    for T, P, i in itertools.product(temperatures, pressures, range(ntasks)):
        newname = '{}_T{}_P{}_part{}'.format(fingerprint, T, P, i+1)
        newdirs.append(newname)
        # Copy over everything
        shutil.copytree(src, newname)

        # Find and modify the simulation.input file
        modify_raspa_input(newname, T, P, ncycles)


def modify_raspa_input(src, T, P, n):
    """Modify the simulation.input file in src

    Parameters
    ----------
    src : string
      Raspa sim directory
    T : float
      temperature
    P : float
      pressure
    n : int
      ncycles
    """
    simfile = os.path.join(src, 'simulation.input')
    # Create backup of old input file, why not..
    os.rename(simfile, simfile + '.bak')

    modifications = {}
    modifications['NumberOfInitializationCycles'] = zero_init
    modifications['NumberOfCycles'] = partial(static_cycles, amount=n)
    modifications['ExternalPressure'] = partial(static_pressure, amount=P)
    modifications['ExternalTemperature'] = partial(static_temperature, amount=T)

    with open(simfile, 'w') as newfile, open(simfile + '.bak', 'r') as oldfile:
        for line in oldfile:
            if line.strip():
                kw = line.split()[0]
                if kw in modifications:
                    line = modifications[kw](line)
            newfile.write(line)


def make_qsubber_script(base, copies):
    with open('qsub_{}.sh'.format(base), 'w') as out:
        out.write("#!/bin/bash\n")
        for d in copies:
            out.write("\n")
            out.write("cd {}\n".format(d))
            out.write("qsub qsub.sh\n")
            out.write("cd ../\n")
