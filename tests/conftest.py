import os
import pytest
import shutil


@pytest.fixture(params=['chk_1234567_part{}', 'chk_1234567_P1.2_part{}'])
def chk_dirs(request, tmpdir):
    template = request.param
    for i in ('1', '2', '3'):
        shutil.copytree(
            'chk_1234567_part{}'.format(i),
            tmpdir.join(template.format(i)).strpath
        )
    with tmpdir.as_cwd():
        # give list of created dirs
        yield [template.format(i) for i in ('1', '2', '3')]


@pytest.fixture(scope='function')
def newdir(tmpdir):
    shutil.copytree('mysim', tmpdir.join('mysim').strpath)
    with tmpdir.as_cwd():
        yield
