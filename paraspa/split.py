"""Splits a single simulation dir into many

"""
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
    newdirs = []

    for i in range(ntasks):
        newname = '{}_part_{}'.format(src, i+1)
        newdirs.append(newname)

        shutil.copytree(src, newname)
