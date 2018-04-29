import numpy as np
import os
import shutil

from . import files
from . import poreblazer


def _filename(fn):
    # grab the last part of a filename
    # this/place/file.txt -> file.txt
    return os.path.split(fn)[-1]


def calc_ncells_required(struc, rcut):
    """Calculate the number of crystal cell replicas required

    Parameters
    ----------
    struc : str
      path to structure
    rcut : float
      cutoff range of forcefield

    Returns
    -------
    nx, ny, nz : int
      number of replicas
    """
    # read cell size and angles of structure
    with open(struc, 'r') as inf:
        dims = poreblazer.grab_dims_from(inf)

    a, b, c = dims['a'], dims['b'], dims['c']
    alpha, beta, gamma = map(np.deg2rad,
                             [dims['alpha'], dims['beta'], dims['gamma']])
    # calculate minimum effective cell length in each dimension
    # this is the length we can increase by tiling in a given direction
    lx = min(abs(a * np.sin(beta)),
             abs(a * np.sin(gamma)))
    ly = min(abs(b * np.sin(alpha)),
             abs(b * np.sin(gamma)))
    lz = min(abs(c * np.sin(beta)),
             abs(c * np.sin(alpha)))

    nx = int(np.ceil(2 * rcut / lx))
    ny = int(np.ceil(2 * rcut / ly))
    nz = int(np.ceil(2 * rcut / lz))

    return nx, ny, nz


def create(structure, gas, forcefield):
    """Create a simulation template

    Parameters
    ----------
    structure : str
      must be either absolute path to file or name in database
    gas, forcefield : str
      must correspond to an existing file

    Returns
    -------
    files : dict
      mapping of filename: content
    """
    if structure.startswith(os.path.sep):
        if not os.path.exists(structure):
            ValueError("Local structure does not exist")
        struc_file = structure
    else:
        struc_file = files.structures[structure.upper()]

    gas_data = files.gases[gas.upper()]
    ff_data = files.forcefields[forcefield.upper()]

    outfiles = dict()

    # calculate cellsize
    cellsize = calc_ncells_required(struc_file, ff_data.cutoff)

    # structure files
    with open(struc_file, 'r') as inf:
        outfiles[_filename(struc_file)] = inf.read()
    with open(gas_data.def_file, 'r') as inf:
        outfiles[_filename(gas_data.def_file)] = inf.read()
    with open(gas_data.pseudo_file, 'r') as inf:
        outfiles['pseudo_atoms.def'] = inf.read()
    with open(ff_data.def_file, 'r') as inf:
        outfiles['force_field_mixing_rules.def'] = inf.read()

    outfiles['framework.def'] = files.FRAMEWORK

    input_template = files.INPUT_TEMPLATE.replace('%%FFNAME%%', forcefield)
    input_template = input_template.replace(
        '%%STRUCTURENAME%%',
        os.path.splitext(_filename(struc_file))[0])
    input_template = input_template.replace('%%GASMOVES%%', gas_data.moves)
    input_template = input_template.replace('%%NCELLS%%',
                                            ' '.join(str(n) for n in cellsize))
    input_template = input_template.replace(
        '%%CUTOFF%%', '{}'.format(ff_data.cutoff))
    outfiles['simulation.input'] = input_template

    return outfiles


def cli_create(structure, gas, forcefield, outdir):
    """Create and write simulation template

    Parameters
    ----------
    structure : str
      either absolute path to structure or name of structure in database
    gas, forcefield : str
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

def grab_structure(structure, outdir=None):
    """Grab a single structure file"""
    struc_file = files.structures[structure.upper()]

    if outdir:
        os.makedirs(outdir)
        outfile = os.path.join(outdir, _filename(struc_file))
    else:
        outfile = _filename(struc_file)
                
    with open(outfile, 'w') as out, open(struc_file, 'r') as inf:
        out.write(inf.read())
