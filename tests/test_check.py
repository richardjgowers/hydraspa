"""
capsys - inbuilt pytest fixture that captures stdout
"""

import pytest

import hydraspa as hrsp


class TestCheck(object):
    def test_child_discovery(self, capsys):
        hrsp.check('chk')
        out, err = capsys.readouterr()

        assert "Found 3 children" in out

    def test_finds_finished(self, capsys):
        hrsp.check('chk')
        out, err = capsys.readouterr()

        assert ' - chk_part1 is FINISHED' in out.split('\n')

    def test_finds_in_progress(self, capsys):
        hrsp.check('chk')
        out, err = capsys.readouterr()

        assert ' - chk_part3 is IN PROGRESS' in out.split('\n')

    def test_finds_incomplete(self, capsys):
        hrsp.check('chk')
        out, err = capsys.readouterr()

        assert ' - chk_part2 is NOT STARTED' in out.split('\n')
