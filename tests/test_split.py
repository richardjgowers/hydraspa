import glob
import os
import shutil
import pytest

import paraspa as prsp

@pytest.fixture
def rm_dirs():
    yield
    for d in glob.glob('*part_*'):
        try:
            shutil.rmtree(d)
        except OSError:
            pass
    try:
        os.remove('qsub_mysim.sh')
    except OSError:
        pass

def runlength(d):
    with open(os.path.join(d, 'simulation.input'), 'r') as f:
        for line in f:
            if 'NumberOfCycles' in line:
                return int(line.split()[1])

# what a qsubber script should look like
REF_QSUB = """\
#!/bin/bash

cd mysim_part_1
qsub qsub.sh
cd ../

cd mysim_part_2
qsub qsub.sh
cd ../
"""

class TestSplit(object):
    FILES = ['file1.txt', 'file2.txt', 'simulation.input']

    @pytest.mark.parametrize('ntasks', [1, 2, 3, 4, 5])
    def test_split_dirs(self, ntasks, rm_dirs):
        prsp.split('mysim', ntasks=ntasks)

        # check that required directories were made
        for i in range(ntasks):
            assert os.path.exists('mysim_part_{}'.format(i + 1))
        assert not os.path.exists('mysim_part_{}'.format(i + 2))

    def test_split_files(self, rm_dirs):
        prsp.split('mysim', ntasks=2)

        # check that each directory made had all the required files

        for d in ('mysim_part_1', 'mysim_part_2'):
            for fn in self.FILES:
                assert os.path.exists(os.path.join(d, fn))

    @pytest.mark.parametrize('ntasks,expected', [
        (2, 500001),
        (3, 333334),
        (4, 250001),
    ])
    def test_check_runlength(self, ntasks, expected, rm_dirs):
        prsp.split('mysim', ntasks=ntasks)

        for d in ('mysim_part_1', 'mysim_part_2'):
            assert runlength(d) == expected

    def test_check_qsubber_made(self, rm_dirs):
        prsp.split('mysim', ntasks=2)

        assert os.path.exists('qsub_mysim.sh')

    def test_check_qsubber_contents(self, rm_dirs):
        prsp.split('mysim', ntasks=2)

        with open('qsub_mysim.sh', 'r') as f:
            assert f.read() == REF_QSUB
