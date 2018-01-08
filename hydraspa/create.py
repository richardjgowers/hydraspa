import numpy as np
import os
import shutil

from . import files
from . import poreblazer


def _filename(fn):
    return os.path.split(fn)[-1]


def calc_ncells_required(struc, rcut):
    """Calculate the number of crystal cell replicas required

    Parameters
    ----------
    struc : str
      name of structure
    rcut : float
      cutoff range of forcefield

    Returns
    -------
    nx, ny, nz : int
      number of replicas
    """
    # read cell size and angles of structure
    with open(files.structures[struc], 'r') as inf:
        dims = poreblazer.grab_dims_from(inf)

    nx = int(np.ceil(2 * rcut / (np.sin(dims['alpha']) * dims['lx'])))
    ny = int(np.ceil(2 * rcut / (np.sin(dims['beta']) * dims['ly'])))
    nz = int(np.ceil(2 * rcut / (np.sin(dims['gamma']) * dims['lz'])))

    return nx, ny, nz


def create(structure, gas, forcefield):
    """Create a simulation template

    Parameters
    ----------
    structure, gas, forcefield : str
      must correspond to an existing file

    Returns
    -------
    files : dict
      mapping of filename: content
    """
    struc_file = files.structures[structure.upper()]
    gas_files = files.gases[gas.upper()]
    ff_file = files.forcefields[forcefield.upper()]

    outfiles = dict()

    # calculate cellsize
    cellsize = calc_ncells_required(structure.upper(), 11.0)

    # structure files
    with open(struc_file, 'r') as inf:
        outfiles[_filename(struc_file)] = inf.read()
    with open(gas_files[0], 'r') as inf:
        outfiles[_filename(gas_files[0])] = inf.read()
    with open(gas_files[1], 'r') as inf:
        outfiles['pseudo_atoms.def'] = inf.read()
    with open(ff_file, 'r') as inf:
        outfiles['force_field_mixing_rules.def'] = inf.read()

    outfiles['framework.def'] = files.FRAMEWORK

    input_template = files.INPUT_TEMPLATE.replace('%%FFNAME%%', forcefield)
    input_template = input_template.replace(
        '%%STRUCTURENAME%%',
        os.path.splitext(_filename(struc_file))[0])
    input_template = input_template.replace('%%GASNAME%%', gas)
    input_template = input_template.replace('%%NCELLS%%',
                                            ' '.join(str(n) for n in cellsize))
    outfiles['simulation.input'] = input_template

    return outfiles


def cli_create(structure, gas, forcefield, outdir):
    """Create and write simulation template

    Parameters
    ----------
    structure, gas, forcefield : str
      name of components from database
    outdir : str
      path to create the template
    """
    outfiles = create(structure, gas, forcefield)

    os.makedirs(outdir)
    template_dir = os.path.join(outdir, 'template')
    os.makedirs(template_dir)
    for k, v in outfiles.items():
         with open(os.path.join(template_dir, k), 'w') as out:
             out.write(v)
