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


def split(src, temperatures, pressures, ntasks, ncycles):
    """Split simulation in src into various conditions

    Parameters
    ----------
    src : string
      Name of the directory we wish to copy
    temperatures : list
      List of temperatures (in K) to create
    pressures : list
      Specify a list of pressures (in kPa) to create
    ntasks : int
      Number of copies of *src* to make
    ncycles : int
      Manually set the number of cycles per simulation.
    """
    if not os.path.exists(os.path.join(src, 'template')):
        raise ValueError("Template not found")

    olddir = os.getcwd()
    os.chdir(src)
    try:
        for T, P, i in itertools.product(temperatures, pressures, range(ntasks)):
            newname = 'T{}_P{}_part{}'.format(T, P, i+1)
            # Copy over everything
            shutil.copytree('template', newname)

            # Find and modify the simulation.input file
            modify_raspa_input(newname, T, P, ncycles)
    finally:
        os.chdir(olddir)


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
