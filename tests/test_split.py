import os

import paraspa as prsp

class TestSplit(object):
    FILES = ['file1.txt', 'file2.txt']

    def test_split_dirs(self):
        prsp.split('mysim', ntasks=2)

        # check that required directories were made
        for i in ['1', '2']:
            assert os.path.exists('mysim_part_{}'.format(i))

    def test_split_files(self):
        prsp.split('mysim', ntasks=2)

        for d in ('mysim_part_1', 'mysim_part_2'):
            for fn in self.FILES:
                assert os.path.exists(os.path.join(d, fn))
