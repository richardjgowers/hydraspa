"""Submodule of included structures and gases

"""

from functools import partial
import glob
from pkg_resources import resource_filename, resource_listdir
import os
import re

def _struc_rf(fn):
    return resource_filename(__package__, os.path.join('structures', fn))

def structure_name(filename):
    try:
        # will strip _clean etc from filenames to give CSD reference
        return re.search('(\w+?)(?:_.+?)?.cif', filename).groups()[0]
    except:
        # some non CSD filenames included in coremof
        return filename

# map structure name to file path
structures = {
    structure_name(fn): _struc_rf(fn)
    for fn in resource_listdir(__package__, 'structures')
}

gases = dict()

forcefields = {
    'UFF': resource_filename(__package__, os.path.join('forcefields', 'uff.def'))
}
