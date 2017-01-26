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

    def test_finds_finished(self):
        pass

    def test_finds_incomplete(self):
        pass

    def test_reports_all_finished(self):
        pass
