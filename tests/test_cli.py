import contextlib
from docopt import docopt
import glob
import itertools
import os
import pytest
import shutil
import subprocess

from hydraspa.cli import __doc__ as doc


def runlength(d):
    with open(os.path.join(d, 'simulation.input'), 'r') as f:
        for line in f:
            if 'NumberOfCycles' in line:
                return int(line.split()[1])

def pressure(d):
    with open(os.path.join(d, 'simulation.input'), 'r') as f:
        for line in f:
            if 'ExternalPressure' in line:
                return float(line.split()[1])

def call(command):
    subprocess.call(command.split())


@pytest.mark.usefixtures('newdir')
class TestCLI(object):
    @pytest.mark.parametrize('path', ['mysim', 'mysim/'])
    @pytest.mark.parametrize('ntasks', ['2', '3', '4'])
    def test_cli(self, path, ntasks):
        cmd = 'hydraspa split {path} -n {n}'.format(path=path, n=ntasks)
        call(cmd)

        # check we made enough sub folders
        assert len(glob.glob('mysim*part*')) == int(ntasks)
        # check the qsubber script was made
        assert os.path.exists('qsub_mysim.sh')
        # check the passport was made
        assert len(glob.glob('mysim*.tar.gz')) == 1

    @pytest.mark.parametrize('path', ['mysim', 'mysim/'])
    @pytest.mark.parametrize('pstyle', ['-P', '--pressures'])
    @pytest.mark.parametrize('pressures',
        ['11.1 10000 30000', '11.1 10k 0.03M', '0.0111k 10000 30k']
    )
    def test_pressure_cli(self, path, pstyle, pressures):
        cmd = 'hydraspa split {path} -n 2 {psty} {pressures}'.format(
            path=path, psty=pstyle, pressures=pressures)
        call(cmd)

        assert len(glob.glob('mysim_4033d12_P*_part*')) == 6
        assert pressure('mysim_4033d12_P11.1_part1') == 11.1
        assert pressure('mysim_4033d12_P10000.0_part1') == 10000.
        assert pressure('mysim_4033d12_P30000.0_part1') == 30000.

    @pytest.mark.parametrize('path', ['mysim', 'mysim/'])
    @pytest.mark.parametrize('cycles', ['-c', '--ncycles'])
    @pytest.mark.parametrize('ncycles', ['900000', '900k', '0.9M'])
    def test_cycles_cli(self, path, cycles, ncycles):
        cmd = 'hydraspa split {path} -n 2 {cyc} {ncyc}'.format(
            path=path, cyc=cycles, ncyc=ncycles)
        call(cmd)

        for d in ['mysim_4033d12_part1', 'mysim_4033d12_part2']:
            assert runlength(d) == 900000


class TestDocopt(object):
    def test_default_ntasks(self):
        args = docopt(doc, 'split this'.split())

        assert args['--ntasks'] == '1'

    @pytest.mark.parametrize('taskstyle', ['-n', '--ntasks'])
    @pytest.mark.parametrize('ntasks', ['2', '3', '4'])
    def test_ntasks(self, taskstyle, ntasks):
        cmdstr = 'split this {} {}'.format(taskstyle, ntasks)

        args = docopt(doc, cmdstr.split())

        assert args['--ntasks'] == ntasks
        assert not args['--pressures']

    @pytest.mark.parametrize('taskstyle', ['-n', '--ntasks'])
    @pytest.mark.parametrize('ntasks', ['2', '3'])
    @pytest.mark.parametrize('pressurestyle', ['-P', '--pressures'])
    @pytest.mark.parametrize('pressures', ['10 20 30', '5 10 20'])
    def test_pressures(self, taskstyle, ntasks, pressurestyle, pressures):
        cmdstr = 'split this {} {} {} {}'.format(taskstyle, ntasks,
                                                 pressurestyle, pressures)
        args = docopt(doc, cmdstr.split())

        assert args['--ntasks'] == ntasks
        assert args['--pressures']
        assert args['<P>'] == pressures.split()

    @pytest.mark.parametrize('cyclestyle', ['-c', '--ncycles'])
    @pytest.mark.parametrize('ncycles', ['100', '250'])
    def test_ncycles(self, cyclestyle, ncycles):
        cmdstr = 'split this -n 2 {} {} -P 10 20'.format(cyclestyle, ncycles)

        args = docopt(doc, cmdstr.split())

        assert args['--ncycles'] == ncycles

    @pytest.mark.parametrize('tasks', ['', '-n 2', '--ntasks 2'])
    @pytest.mark.parametrize('cycles', ['', '-c 1234', '--ncycles 1234'])
    @pytest.mark.parametrize('pressures', ['', '-P 10 20', '--pressures 10 20'])
    @pytest.mark.parametrize('order', itertools.permutations(range(3), 3))
    def test_reordering(self, tasks, cycles, pressures, order):
        opts = [tasks, cycles, pressures]

        cmdstr = 'split this ' + ' '.join(opts[i] for i in order)
        args = docopt(doc, cmdstr.split())

        if tasks:
            assert args['--ntasks'] == '2'
        else:
            assert args['--ntasks'] == '1'
        if cycles:
            assert args['--ncycles'] == '1234'
        else:
            assert not args['--ncycles']
        if pressures:
            assert args['<P>'] == ['10', '20']
        else:
            assert not args['--pressures']
