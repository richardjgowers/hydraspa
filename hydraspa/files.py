"""Submodule of included structures and gases

"""

from collections import namedtuple
from functools import partial
import glob
from pkg_resources import resource_filename, resource_listdir
import os
import re

_rf = partial(resource_filename, __package__)

def _struc_rf(fn):
    return _rf(os.path.join('structures', fn))

def structure_name(filename):
    try:
        # will strip '_clean' etc from filenames to give CSD reference
        return re.match('^(\w+?)(?:_.+?)?.cif', filename).groups()[0]
    except:
        # some non CSD filenames included in coremof
        return os.path.splitext(filename)[0]

# map structure name to file path
structures = {
    structure_name(fn).upper(): _struc_rf(fn)
    for fn in resource_listdir(__package__, 'structures')
}


SINGLE_SITE_MOVES = """\
Component 0 MoleculeName             {}
            TranslationProbability   0.25
            SwapProbability          0.75
            CreateNumberOfMolecules  0
"""

MULTI_SITE_MOVES = """\
Component 0 MoleculeName             {}
            TranslationProbability   0.25
            RotationProbability      0.25
            SwapProbability          0.50
            CreateNumberOfMolecules  0
"""

GasSpecies = namedtuple('GasSpecies', ['def_file', 'pseudo_file', 'moves'])

_SINGLE_SITE = ['Ar', 'helium']
_MULTI_SITE = ['CO2', 'N2']

gases = dict()
for nm in _SINGLE_SITE + _MULTI_SITE:
    MOVES = SINGLE_SITE_MOVES if nm in _SINGLE_SITE else MULTI_SITE_MOVES

    gases[nm.upper()] = GasSpecies(
        def_file=_rf(os.path.join('gases', nm + '.def')),
        pseudo_file=_rf(os.path.join('gases', 'pseudo_' + nm + '.def')),
        moves=MOVES.format(nm)
    )

Forcefield = namedtuple('Forcefield', ['def_file', 'cutoff'])
forcefields = {
    'UFF': Forcefield(
        def_file=_rf(os.path.join('forcefields', 'uff.def')),
        cutoff=12.8
    )
}


FRAMEWORK = """\
#CoreShells bond  BondDipoles UreyBradley bend  inv  tors improper-torsion bond/bond bond/bend bend/bend stretch/torsion bend/torsion
          0    0            0           0    0    0     0                0         0         0         0               0            0
"""

INPUT_TEMPLATE = """\
SimulationType                MonteCarlo
NumberOfCycles                100000
NumberOfInitializationCycles  0
PrintEvery                    100
PrintPropertiesEvery          100
RestartFile                   no

# Restart and crash-recovery
# Write a binary file (binary restart.dat).
ContinueAfterCrash              no
# The output frequency of the crash-recovery file.
WriteBinaryRestartFileEvery     0

Forcefield                    %%FFNAME%%
CutOffVDW                     %%CUTOFF%%
ChargeMethod                  Ewald
CutOffChargeCharge            %%CUTOFF%%
EwaldPrecision                1e-6
UseChargesFromCIFFile         yes

Framework 0
FrameworkName %%STRUCTURENAME%%
UnitCells %%NCELLS%%
HeliumVoidFraction 0.78
ExternalTemperature %%TEMPERATURE%%
ExternalPressure    %%PRESSURE%%
Movies no
WriteMoviesEvery    0

# Grids
NumberOfGrids 0

# Gas molecule MC moves section
%%GASMOVES%%


"""
