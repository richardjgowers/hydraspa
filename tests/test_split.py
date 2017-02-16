import glob
import os
import shutil
import pytest

import hydraspa as hrsp


def runlength(d):
    with open(os.path.join(d, 'simulation.input'), 'r') as f:
        for line in f:
            if 'NumberOfCycles' in line:
                return int(line.split()[1])

def eq_length(d):
    with open(os.path.join(d, 'simulation.input'), 'r') as f:
        for line in f:
            if 'NumberOfInitializationCycles' in line:
                return int(line.split()[1])


def pressure(d):
    with open(os.path.join(d, 'simulation.input'), 'r') as f:
        for line in f:
            if 'ExternalPressure' in line:
                return float(line.split()[1])

# what a qsubber script should look like
REF_QSUB = """\
#!/bin/bash

cd mysim_1234567_part1
qsub qsub.sh
cd ../

cd mysim_1234567_part2
qsub qsub.sh
cd ../
"""

@pytest.mark.usefixtures('newdir')
class TestSplit(object):
    FILES = ['file1.txt', 'file2.txt', 'simulation.input']

    @pytest.mark.parametrize('ntasks', [1, 2, 3, 4, 5])
    def test_split_dirs(self, ntasks):
        hrsp.split('mysim', '1234567', ntasks=ntasks)

        # check that required directories were made
        for i in range(ntasks):
            assert os.path.exists('mysim_1234567_part{}'.format(i + 1))
        assert not os.path.exists('mysim_1234567_part{}'.format(i + 2))

    def test_split_files(self):
        hrsp.split('mysim', '1234567', ntasks=2)

        # check that each directory made had all the required files

        for d in ('mysim_1234567_part1', 'mysim_1234567_part2'):
            for fn in self.FILES:
                assert os.path.exists(os.path.join(d, fn))

    @pytest.mark.parametrize('ntasks,ncycles,expected', [
        (2, None, 500001),  # divide 1M cycles by ntasks (+1)
        (3, None, 333334),
        (4, None, 250001),
        (2, 10000, 10000),  # override division thingy
        (4, 25000, 25000),
    ])
    def test_check_runlength(self, ntasks, ncycles, expected):
        hrsp.split('mysim', '1234567', ntasks=ntasks, ncycles=ncycles)

        assert len(glob.glob('mysim_1234567_part*')) == ntasks
        for d in glob.glob('mysim_1234567_part*'):
            assert runlength(d) == expected

    def test_eq_length(self):
        # hack the equilibration length to be 100
        with open('mysim/simulation.input', 'r') as inf, open('new', 'w') as new:
            for line in inf:
                if line.startswith('NumberOfInit'):
                    line = 'NumberOfInitializationCycles  100\n'
                new.write(line)
        shutil.move('new', 'mysim/simulation.input')

        hrsp.split('mysim', '1234567', ntasks=2, ncycles=100)

        for d in glob.glob('mysim_1234567_part*'):
            assert eq_length(d) == 0

    def test_check_qsubber_made(self):
        hrsp.split('mysim', '1234567', ntasks=2)

        assert os.path.exists('qsub_mysim.sh')

    def test_check_qsubber_contents(self):
        hrsp.split('mysim', '1234567', ntasks=2)

        with open('qsub_mysim.sh', 'r') as f:
            assert f.read() == REF_QSUB

    @pytest.mark.parametrize('ntasks', [1, 2])
    @pytest.mark.parametrize('p', [[5, 10, 20], [5.5, 10, 20]])
    def test_pressures(self, ntasks, p):
        hrsp.split('mysim', '1234567', ntasks=ntasks, pressures=p)

        assert len(glob.glob('mysim_1234567_P*_part*')) == ntasks * len(p)
        assert os.path.exists('mysim_1234567_P10_part1')

        # check runlengths
        # check pressures
        assert pressure('mysim_1234567_P10_part1') == 10.0
