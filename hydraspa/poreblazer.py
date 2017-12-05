"""Preparing Poreblazer inputs


"""
import os
from pkg_resources import resource_filename
import shutil

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
    # load cif file
    with open(files.structures[structure_name], 'r') as i:
        structure = i.readlines()
        
    # grab xyz from cif file
    xyz = grab_xyz_from(structure)

    # grab dimensions from cif file
    dims = grab_dims_from(structure)

    # write xyz file
    xyzname = structure_name + '.xyz'
    write_xyz_file(xyzname, xyz)

    # write input.dat file
    with open('input.dat', 'w') as out:
        out.write('{}\n'.format(xyzname))
        out.write('{} {} {}\n'.format(
            dims['lx'], dims['ly'], dims['lz']))
        out.write('{} {} {}\n'.format(
            dims['alpha'], dims['beta'], dims['gamma']))

    # write UFF.atoms
    shutil.copy(UFF_ATOMS, '.')
    # write defaults.dat
    shutil.copy(DEFAULTS_DAT, '.')


def write_xyz_file(name, contents):
    with open(name, 'w') as out:
        out.write('{}\n\n'.format(len(contents)))
        for nm, x, y, z in contents:
            out.write('{} {} {} {}\n'.format(nm, x, y, z))

    
def grab_xyz_from(struc):
    read_positions = False
    xyz = []
        
    for line in struc:
        if read_positions:
            if not line.strip():
                # if we're at the end of positions
                break
            else:
                xyz.append(line.split()[:4])
        elif line.lstrip().startswith('_atom_site_charge'):
            read_positions = True

    return xyz


def grab_dims_from(struc):
    dims = dict()
    for line in struc:
        if line.lstrip().startswith('_cell_length_a'):
            dims['lx'] = float(line.split()[1])
        elif line.lstrip().startswith('_cell_length_b'):
            dims['ly'] = float(line.split()[1])
        elif line.lstrip().startswith('_cell_length_c'):
            dims['lz'] = float(line.split()[1])
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
