import contextlib
from docopt import docopt
import glob
import itertools
import os
import pytest
import shutil
import subprocess

from hydraspa.cli import __doc__ as doc


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
    @pytest.mark.parametrize('pressures', ['10 20 30', '10 20'])
    def test_pressure_cli(self, path, pressures):
        cmd = 'hydraspa split {path} -n 2 -P {pressures}'.format(
            path=path, pressures=pressures)
        call(cmd)

        assert len(glob.glob('mysim_P*_part*')) == len(pressures.split()) * 2


class TestDocopt(object):
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

    @pytest.mark.parametrize('taskstyle', ['-n', '--ntasks'])
    @pytest.mark.parametrize('pressurestyle', ['-P', '--pressures'])
    @pytest.mark.parametrize('cyclestyle', ['-c', '--ncycles'])
    @pytest.mark.parametrize('order', itertools.permutations(range(3), 3))
    def test_reordering(self, taskstyle, pressurestyle, cyclestyle, order):
        a = '{} 2'.format(taskstyle)
        b = '{} 1234'.format(cyclestyle)
        c = '{} 10 20'.format(pressurestyle)
        opts = [a, b, c]

        cmdstr = 'split this ' + ' '.join(opts[i] for i in order)
        args = docopt(doc, cmdstr.split())

        assert args['--ntasks'] == '2'
        assert args['--ncycles'] == '1234'
        assert args['<P>'] == ['10', '20']
        
