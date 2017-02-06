"""
capsys - inbuilt pytest fixture that captures stdout
"""

import pytest

import hydraspa as hrsp


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

