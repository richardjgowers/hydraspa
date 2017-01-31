"""Splits a single simulation dir into many

"""
from __future__ import division

from functools import partial
import os
import shutil


def static_cycles(line, amount):
    return 'NumberOfCycles {}\n'.format(amount)

def divide_cycles(line, factor):
    ncycles = line.split()[1]

    newcycles = 1 + (int(ncycles) // factor)

    return line.replace(ncycles, str(newcycles))
    

def split(src, ntasks, ncycles=None):
    """Split simulation in *src* into *ntasks*

    Parameters
    ----------
    src : string
      Name of the directory we wish to copy
    ntasks : int
      Number of copies of *src* to make
    ncycles : int, optional
      Manually set the number of cycles per simulation.  Otherwise
      use existing amount / ntasks
    """
    src = src.strip('/')

    newdirs = []

    for i in range(ntasks):
        newname = '{}_part_{}'.format(src, i+1)
        newdirs.append(newname)
        # Copy over everything
        shutil.copytree(src, newname)

        # Find and modify the simulation.input file
        modifications = {}
        if ncycles is None:
            modifications['NumberOfCycles'] = partial(divide_cycles, factor=ntasks)
        else:
            modifications['NumberOfCycles'] = partial(static_cycles, amount=ncycles)

        modify_raspa_input(newname, modifications)

    make_qsubber_script(src, newdirs)


def modify_raspa_input(src, mods):
    """Modify the simulation.input file in *src* according to *mods*

    Parameters
    ----------
    src : string
      Raspa sim directory
    mods : dict
      Maps keywords to a function applied to the entire line, which
      returns a replacement line
    """
    simfile = os.path.join(src, 'simulation.input')
    # Create backup of old input file, why not..
    os.rename(simfile, simfile + '.bak')

    with open(simfile, 'w') as newfile, open(simfile + '.bak', 'r') as oldfile:
        for line in oldfile:
            if line.strip():
                kw = line.split()[0]
                if kw in mods:
                    line = mods[kw](line)
            newfile.write(line)

def make_qsubber_script(base, copies):
    with open('qsub_{}.sh'.format(base), 'w') as out:
        out.write("#!/bin/bash\n")
        for d in copies:
            out.write("\n")
            out.write("cd {}\n".format(d))
            out.write("qsub qsub.sh\n")
            out.write("cd ../\n")
