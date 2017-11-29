import numpy as np
import os
import shutil

from . import files


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
    lengths = {}
    angles = {}

    with open(struc, 'r') as inf:
        for line in inf:
            if line.startswith('_cell_length_a'):
                lengths['a'] = float(line.split()[1])
            elif line.startswith('_cell_length_b'):
                lengths['b'] = float(line.split()[1])
            elif line.startswith('_cell_length_c'):
                lengths['c'] = float(line.split()[1])
            elif line.startswith('_cell_angle_alpha'):
                angles['alpha'] = np.deg2rad(float(line.split()[1]))
            elif line.startswith('_cell_angle_beta'):
                angles['beta'] = np.deg2rad(float(line.split()[1]))
            elif line.startswith('_cell_angle_gamma'):
                angles['gamma'] = np.deg2rad(float(line.split()[1]))

            if (len(lengths) + len(angles)) == 6:
                break

    nx = int(np.ceil(2 * rcut / (np.sin(angles['alpha']) * lengths['a'])))
    ny = int(np.ceil(2 * rcut / (np.sin(angles['beta']) * lengths['b'])))
    nz = int(np.ceil(2 * rcut / (np.sin(angles['gamma']) * lengths['c'])))

    return nx, ny, nz


def create(structure, gas, forcefield, outdir):
    """Create a simulation template

    Parameters
    ----------
    structure, gas, forcefield : str
      must correspond to an existing file
    outdir : str
      where to put the template
    """
    struc_file = files.structures[structure.upper()]
    gas_files = files.gases[gas.upper()]
    ff_file = files.forcefields[forcefield.upper()]

    # calculate cellsize
    cellsize = calc_ncells_required(struc_file, 11.0)

    os.makedirs(outdir)
    # structure files
    shutil.copy(struc_file,
                os.path.join(outdir, _filename(struc_file)))
    shutil.copy(gas_files[0],
                os.path.join(outdir, _filename(gas_files[0])))
    shutil.copy(gas_files[1],
                os.path.join(outdir, 'pseudo_atoms.def'))
    shutil.copy(ff_file,
                os.path.join(outdir, 'force_field_mixing_rules.def'))
    with open(os.path.join(outdir, 'framework.def'), 'w') as out:
        out.write(files.FRAMEWORK)
    input_template = files.INPUT_TEMPLATE.replace('%%FFNAME%%', forcefield)
    input_template = input_template.replace(
        '%%STRUCTURENAME%%',
        os.path.splitext(_filename(struc_file))[0])
    input_template = input_template.replace('%%GASNAME%%', gas)
    input_template = input_template.replace('%%NCELLS%%',
                                            ' '.join(str(n) for n in cellsize))
    with open(os.path.join(outdir, 'simulation.input'), 'w') as out:
        out.write(input_template)
