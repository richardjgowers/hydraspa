"""
capsys - inbuilt pytest fixture that captures stdout
"""

import pytest
import shutil

import hydraspa as hrsp


@pytest.fixture
def chk_dirs(tmpdir):
    shutil.copytree('chk', tmpdir.join('chk').strpath)

    with tmpdir.as_cwd():
        yield ('chk/T100.0_P123.0_part1',
               'chk/T100.0_P123.0_part2',
               'chk/T100.0_P123.0_part3')


class TestCheck(object):
    def test_child_discovery(self, capsys, chk_dirs):
        hrsp.check('chk')
        out, err = capsys.readouterr()

        assert "Found 3 children" in out

    def test_finds_finished(self, capsys, chk_dirs):
        hrsp.check('chk')
        out, err = capsys.readouterr()

        dirs = chk_dirs

        assert ' - {} is FINISHED'.format(dirs[0]) in out.split('\n')

    def test_finds_in_progress(self, capsys, chk_dirs):
        hrsp.check('chk')
        out, err = capsys.readouterr()

        dirs = chk_dirs

        assert ' - {} is IN PROGRESS'.format(dirs[2]) in out.split('\n')

    def test_finds_incomplete(self, capsys, chk_dirs):
        hrsp.check('chk')
        out, err = capsys.readouterr()

        dirs = chk_dirs

        assert ' - {} is NOT STARTED'.format(dirs[1]) in out.split('\n')
