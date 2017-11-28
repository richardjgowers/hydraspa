import os
import shutil

from . import files


def _filename(fn):
    return os.path.split(fn)[-1]


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
    with open(os.path.join(outdir, 'simulation.input'), 'w') as out:
        out.write(input_template)
