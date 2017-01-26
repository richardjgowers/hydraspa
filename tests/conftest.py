import glob
import os
import pytest
import shutil


@pytest.fixture(scope='function')
def rm_dirs():
    yield
    for d in glob.glob('mysim_part_*'):
        try:
            shutil.rmtree(d)
        except OSError:
            pass
    try:
        os.remove('qsub_mysim.sh')
    except OSError:
        pass
