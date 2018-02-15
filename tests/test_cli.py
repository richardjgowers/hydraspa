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


def temperature(d):
    with open(os.path.join(d, 'simulation.input'), 'r') as f:
        for line in f:
            if 'ExternalTmperature' in line:
                return float(line.split()[1])

def call(command):
    subprocess.call(command.split())


@pytest.mark.usefixtures('newdir')
class TestCLI(object):
    @pytest.mark.parametrize('path', ['mysim', 'mysim/'])
    @pytest.mark.parametrize('ntasks', ['2', '3', '4'])
    def test_cli(self, path, ntasks):
        cmd = 'hydraspa split {path} -n {n} -P 10 -T 208.0 -c 20k'.format(
            path=path, n=ntasks)
        call(cmd)

        # check we made enough sub folders
        assert len(glob.glob('mysim/*part*')) == int(ntasks)

    @pytest.mark.parametrize('pstyle', ['-P'])
    @pytest.mark.parametrize('pressures',
        ['11.1,10000,30000', '11.1,10k,0.03M', '0.0111k,10000,30k']
    )
    def test_pressure_cli(self, pstyle, pressures):
        cmd = 'hydraspa split mysim {psty} {pressures} -T 208.0 -c 20k -n 2'.format(
            psty=pstyle, pressures=pressures)
        call(cmd)

        assert len(glob.glob('mysim/T*_P*_part*')) == 6
        assert pressure('mysim/T208.0_P11.1_part1') == 11.1
        assert pressure('mysim/T208.0_P10000.0_part1') == 10000.
        assert pressure('mysim/T208.0_P30000.0_part1') == 30000.

    @pytest.mark.parametrize('path', ['mysim', 'mysim/'])
    @pytest.mark.parametrize('cycles', ['-c'])
    @pytest.mark.parametrize('ncycles', ['900000', '900k', '0.9M'])
    def test_cycles_cli(self, path, cycles, ncycles):
        cmd = 'hydraspa split {path} -P 10.0 -T 208.0 {cyc} {ncyc} -n 2'.format(
            path=path, cyc=cycles, ncyc=ncycles)
        call(cmd)

        for d in ['mysim/T208.0_P10.0_part1', 'mysim/T208.0_P10.0_part2']:
            assert runlength(d) == 900000


class TestDocopt(object):
    def test_default_ntasks(self):
        args = docopt(doc, 'split this -P 10 -T 208 -c 40'.split())

        assert args['-n'] == '1'

    @pytest.mark.parametrize('ntasks', ['2', '3', '4'])
    def test_ntasks(self, ntasks):
        cmdstr = 'split this -P 10 -T 200 -c 40 -n {}'.format(ntasks)

        args = docopt(doc, cmdstr.split())

        assert args['-n'] == ntasks

    @pytest.mark.parametrize('pressures', ['10,20,30', '5,10,20'])
    def test_pressures(self, pressures):
        cmdstr = 'split this -P {} -T 208.0 -c 20k'.format(pressures)
        args = docopt(doc, cmdstr.split())

        assert args['-P'] == pressures

    @pytest.mark.parametrize('ncycles', ['100', '250'])
    def test_ncycles(self, ncycles):
        cmdstr = 'split this -c {} -P 10,20 -T 200,300'.format(ncycles)

        args = docopt(doc, cmdstr.split())

        assert args['-c'] == ncycles

    @pytest.mark.parametrize('tasks', ['', '-n 2'])
    @pytest.mark.parametrize('cycles', ['-c 1234'])
    @pytest.mark.parametrize('pressures', ['-P 10,20'])
    @pytest.mark.parametrize('temperatures', ['-T 200'])
    @pytest.mark.parametrize('order', itertools.permutations(range(4), 4))
    def test_reordering(self, tasks, cycles, pressures, temperatures, order):
        opts = [tasks, cycles, pressures, temperatures]

        cmdstr = 'split this ' + ' '.join(opts[i] for i in order)
        args = docopt(doc, cmdstr.split())

        if tasks:
            assert args['-n'] == '2'
        else:
            assert args['-n'] == '1'
        assert args['-c'] == '1234'
        assert args['-P'] == '10,20'
        assert args['-T'] == '200'
