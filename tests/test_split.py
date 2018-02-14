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


@pytest.mark.usefixtures('newdir')
class TestSplit(object):
    @pytest.mark.parametrize('ntasks', [1, 2, 3, 4, 5])
    def test_split_ntasks(self, ntasks):
        # check varying ntasks
        hrsp.split(src='mysim', temperatures=[100.0],
                   pressures=[1234.0], ncycles=10000,
                   ntasks=ntasks)

        # check that required directories were made
        for i in range(ntasks):
            assert os.path.exists(
                os.path.join('mysim', 'T100.0_P1234.0_part{}'.format(i + 1)))
        assert not os.path.exists(
            os.path.join('mysim', 'T100.0_P1234.0_part{}'.format(i + 2)))

    def test_split_files(self):
        # check that each directory made had all the required files
        hrsp.split(src='mysim', temperatures=[100.0],
                   pressures=[1234.0], ncycles=10000,
                   ntasks=2)

        root = os.path.join('mysim', 'T100.0_P1234.0_part{}')

        for d in (root.format(1), root.format(2)):
            for fn in ['file1.txt', 'file2.txt', 'simulation.input']:
                assert os.path.exists(os.path.join(d, fn))

    def test_eq_length(self):
        # hack the equilibration length to be 100
        with open('mysim/template/simulation.input', 'r') as inf:
            with open('new', 'w') as new:
                for line in inf:
                    if line.startswith('NumberOfInit'):
                        line = 'NumberOfInitializationCycles  100\n'
                    new.write(line)
        shutil.move('new', 'mysim/template/simulation.input')

        hrsp.split(src='mysim', temperatures=[100.0],
                   pressures=[1234.0], ncycles=10000,
                   ntasks=2)

        for d in glob.glob('mysim_T100.0_P1234.0_part*'):
            assert eq_length(d) == 0

    @pytest.mark.parametrize('p', [[5, 10, 20], [5.5, 10, 20]])
    def test_pressures(self, p):
        hrsp.split('mysim', temperatures=[100.0], pressures=p,
                   ntasks=1, ncycles=1000)

        assert len(glob.glob('mysim/T100.0_P*_part1')) == len(p)

        # check runlengths
        # check pressures
        assert pressure('mysim/T100.0_P10_part1') == 10.0
