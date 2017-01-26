"""
capsys - inbuilt pytest fixture that captures stdout
"""

import pytest

import paraspa as prsp


class TestCheck(object):
    def test_child_discovery(self, capsys):
        prsp.check('chk')
        out, err = capsys.readouterr()

        assert "Found 3 children" in out

    def test_finds_finished(self, capsys):
        prsp.check('chk')
        out, err = capsys.readouterr()

        assert ' - chk_part_1 is FINISHED' in out.split('\n')

    def test_finds_in_progress(self, capsys):
        prsp.check('chk')
        out, err = capsys.readouterr()

        assert ' - chk_part_3 is IN PROGRESS' in out.split('\n')

    def test_finds_incomplete(self, capsys):
        prsp.check('chk')
        out, err = capsys.readouterr()

        assert ' - chk_part_2 is NOT STARTED' in out.split('\n')
