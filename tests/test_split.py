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

class TestSplit(object):
    FILES = ['file1.txt', 'file2.txt']

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
