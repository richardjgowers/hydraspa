import os
import pytest

import hydraspa


@pytest.mark.parametrize('val,conv,expected', [
    ('12', int, 12),
    ('10k', int, 10000),
    ('5.4k', int, 5400),
    ('0.9M', int, 900000),
    ('42', float, 42.0),
    ('1.2345k', float, 1234.5),
    ('7.7M', float, 7.7e6),
])
def test_conv_to_number(val, conv, expected):
    answer = hydraspa.util.conv_to_number(val, conv)

    assert isinstance(answer, conv)
    assert answer == expected

def test_conv_fail():
    with pytest.raises(ValueError):
        hydraspa.util.conv_to_number('5.4q', float)


@pytest.fixture()
def discover(tmpdir):
    tmpdir.mkdir('mysim')
    tmpdir.mkdir('mysim', 'template')

    for T in [100.0, 200.0]:
        for P in [10.0, 20.0]:
            tmpdir.mkdir('mysim', 'T{}_P{}_part1'.format(T, P))

    with tmpdir.as_cwd():
        yield 'mysim'


def test_discover(discover):
    results = hydraspa.util.discover('mysim')

    assert len(results) == 4

    assert results[0].path == 'mysim/T100.0_P10.0_part1'
    assert results[0].temperature == 100.0
    assert results[0].pressure == 10.0
    assert results[0].partnumber == 1
