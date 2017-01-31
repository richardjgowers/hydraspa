import contextlib
import os
import pytest
import shutil


@contextlib.contextmanager
def indir(d):
    olddir = os.getcwd()
    os.chdir(d)
    try:
        yield
    finally:
        os.chdir(olddir)


@pytest.fixture(scope='function')
def newdir(tmpdir):
    shutil.copytree('mysim', tmpdir.join('mysim').strpath)
    shutil.copy('premade_mysim.tar.gz', tmpdir.strpath)
    with indir(tmpdir.strpath):
        yield
