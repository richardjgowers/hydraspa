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

def runlength(d):
    with open(os.path.join(d, 'simulation.input'), 'r') as f:
        for line in f:
            if 'NumberOfCycles' in line:
                return int(line.split()[1])

class TestSplit(object):
    FILES = ['file1.txt', 'file2.txt', 'simulation.input']

    def test_split_dirs(self, rm_dirs):
        prsp.split('mysim', ntasks=2)

        # check that required directories were made
        for i in ['1', '2']:
            assert os.path.exists('mysim_part_{}'.format(i))

    def test_split_files(self, rm_dirs):
        prsp.split('mysim', ntasks=2)

        # check that each directory made had all the required files

        for d in ('mysim_part_1', 'mysim_part_2'):
            for fn in self.FILES:
                assert os.path.exists(os.path.join(d, fn))

    def test_check_runlength(self, rm_dirs):
        prsp.split('mysim', ntasks=2)

        for d in ('mysim_part_1', 'mysim_part_2'):
            assert runlength(d) == 500001
