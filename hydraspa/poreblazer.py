"""Preparing Poreblazer inputs


"""
import numpy as np
import os
from pkg_resources import resource_filename
import shutil
from MDAnalysis.lib import distances

from . import files

# defaults.dat
DEFAULTS_DAT = resource_filename(
    __package__,
    os.path.join('pb_files', 'defaults.dat')
)

# UFF.atoms
UFF_ATOMS = resource_filename(
    __package__,
    os.path.join('pb_files', 'UFF.atoms')
)


def create_input(structure_name):
    """Create input for Poreblazer

    Creates input for poreblazer in the current directory

    Parameters
    ----------
    structure_name : str
      name of structure from Database
    """
    # load cif file
    with open(files.structures[structure_name.upper()], 'r') as i:
        structure = i.readlines()

    # grab xyz from cif file
    names, xyz = grab_xyz_from(structure)
    # grab dimensions from cif file
    dims = grab_dims_from(structure)
    # convert fractional coordinates to real space
    xyz = fractional_to_real(xyz, dims)

    # write xyz file
    xyzname = structure_name + '.xyz'
    write_xyz_file(xyzname, names, xyz)

    # write input.dat file
    with open('input.dat', 'w') as out:
        out.write('{}\n'.format(xyzname))
        out.write('{} {} {}\n'.format(
            dims['a'], dims['b'], dims['c']))
        out.write('{} {} {}\n'.format(
            dims['alpha'], dims['beta'], dims['gamma']))

    # write UFF.atoms
    shutil.copy(UFF_ATOMS, '.')
    # write defaults.dat
    shutil.copy(DEFAULTS_DAT, '.')


def fractional_to_real(xyz, dims):
    """Convert fractional positions to real positions

    Parameters
    ----------
    xyz : np.ndarray
      fractional positions
    dims : dict
      dict of box information

    Returns
    -------
    xyz : np.ndarray
      real space representation of fractional positions
    """
    box = np.array([dims['a'], dims['b'], dims['c'],
                    dims['alpha'], dims['beta'], dims['gamma']],
                   dtype=np.float32)

    xyz = distances.transform_StoR(xyz, box)

    return distances.apply_PBC(xyz, box)


def write_xyz_file(name, names, positions):
    """Create an xyz file

    Parameters
    ----------
    name : str
      output file name
    names : list
      atom names
    positions : np.ndarray
      positions of atoms
    """
    with open(name, 'w') as out:
        out.write('{}\n\n'.format(len(positions)))
        for nm, (x, y, z) in zip(names, positions):
            out.write('{} {} {} {}\n'.format(nm, x, y, z))


def grab_xyz_from(struc):
    """Extract names and fractional coordinates from CIF data

    Parameters
    ----------
    struc : list of lines
      the read cif file

    Returns
    -------
    names, positions : list, np.ndarray
    """
    read_positions = False
    names = []
    xyz = []

    for line in struc:
        if read_positions:
            if not line.strip():
                # if we're at the end of positions
                break
            else:
                names.append(line.split()[0])
                xyz.append(line.split()[1:4])
        elif line.lstrip().startswith('_atom_site_charge'):
            read_positions = True

    return names, np.array(xyz, dtype=np.float32)


def grab_dims_from(struc):
    """Extract box information from CIF data

    Parameters
    ----------
    struc : list of lines
      the read cif file

    Returns
    -------
    dims : dict
      dict with keys a, b, c, alpha, beta, gamma
    """
    dims = dict()
    for line in struc:
        if line.lstrip().startswith('_cell_length_a'):
            dims['a'] = float(line.split()[1])
        elif line.lstrip().startswith('_cell_length_b'):
            dims['b'] = float(line.split()[1])
        elif line.lstrip().startswith('_cell_length_c'):
            dims['c'] = float(line.split()[1])
        elif line.lstrip().startswith('_cell_angle_alpha'):
            dims['alpha'] = float(line.split()[1])
        elif line.lstrip().startswith('_cell_angle_beta'):
            dims['beta'] = float(line.split()[1])
        elif line.lstrip().startswith('_cell_angle_gamma'):
            dims['gamma'] = float(line.split()[1])

        if len(dims) == 6:
            break
    else:
        raise ValueError('couldnt read dims')

    return dims
