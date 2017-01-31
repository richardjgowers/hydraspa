"""Splits a single simulation dir into many

"""
from __future__ import division

import os
import shutil


def split(src, ntasks):
    """Split simulation in *src* into *ntasks*

    Parameters
    ----------
    src : string
      Name of the directory we wish to copy
    ntasks : int
      Number of copies of *src* to make
    """
    src = src.strip('/')

    newdirs = []

    for i in range(ntasks):
        newname = '{}_part_{}'.format(src, i+1)
        newdirs.append(newname)
        # Copy over everything
        shutil.copytree(src, newname)

        # Find and modify the simulation.input file
        divide_runtime_by(newname, ntasks)

    make_qsubber_script(src, newdirs)


def divide_runtime_by(src, factor):
    """Look in *src* and divide the number of Cycles by *factor*"""
    simfile = os.path.join(src, 'simulation.input')
    # Create backup of old input file, why not..
    os.rename(simfile, simfile + '.bak')

    with open(simfile, 'w') as newfile, open(simfile + '.bak', 'r') as oldfile:
        for line in oldfile:
            if not line.startswith('#') and 'NumberOfCycles' in line:
                # find the number of cycles
                ncycles = line.split()[1]
                # floor division then add one
                # ensures sum of runlengths is always *at least* the same length
                newcycles = 1 + (int(ncycles) // factor)

                line = line.replace(ncycles, str(newcycles))

            newfile.write(line)

def make_qsubber_script(base, copies):
    with open('qsub_{}.sh'.format(base), 'w') as out:
        out.write("#!/bin/bash\n")
        for d in copies:
            out.write("\n")
            out.write("cd {}\n".format(d))
            out.write("qsub qsub.sh\n")
            out.write("cd ../\n")
