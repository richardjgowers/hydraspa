import os
import pytest
import shutil


HERE = os.path.dirname(os.path.abspath(__file__))

@pytest.fixture(scope='function')
def newdir(tmpdir):
    shutil.copytree(os.path.join(HERE, 'mysim'),
                    tmpdir.join('mysim').strpath)
    with tmpdir.as_cwd():
        yield


@pytest.fixture
def chk_dirs(tmpdir):
    shutil.copytree(os.path.join(HERE, 'chk'),
                    tmpdir.join('chk').strpath)

    with tmpdir.as_cwd():
        yield ('chk/T100.0_P123.0_part1',
               'chk/T100.0_P123.0_part2',
               'chk/T100.0_P123.0_part3')
