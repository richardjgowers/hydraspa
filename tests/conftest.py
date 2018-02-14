import os
import pytest
import shutil


@pytest.fixture(scope='function')
def newdir(tmpdir):
    shutil.copytree('mysim', tmpdir.join('mysim').strpath)
    with tmpdir.as_cwd():
        yield
