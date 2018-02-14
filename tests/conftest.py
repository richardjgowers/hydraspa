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


@pytest.fixture(params=['chk_1234567_part{}', 'chk_1234567_P1.2_part{}'])
def chk_dirs(request, tmpdir):
    template = request.param
    for i in ('1', '2', '3'):
        shutil.copytree(
            'chk_1234567_part{}'.format(i),
            tmpdir.join(template.format(i)).strpath
        )
    with indir(tmpdir.strpath):
        # give list of created dirs
        yield [template.format(i) for i in ('1', '2', '3')]


@pytest.fixture(scope='function')
def newdir(tmpdir):
    shutil.copytree('mysim', tmpdir.join('mysim').strpath)
    with indir(tmpdir.strpath):
        yield

@pytest.fixture
def REFHASH():
    return '4033d12'
