import pytest

import hydraspa as hrsp


def test_parser_1():
    res = hrsp.gather.parse_results('gth/T100.0_P400.0_part1')

    assert res.values[0] == 1.5
    assert res.values[1] == 3.0
    assert res.values[2] == 4.5
    assert res.values[3] == 6.0

    assert res.index[0] == 100
    assert res.index[1] == 200
    assert res.index[2] == 300
    assert res.index[3] == 400


def test_parser_2():
    res = hrsp.gather.parse_results('gth/T100.0_P800.0_part1')

    assert res.values[0] == 6.0
    assert res.values[1] == 7.0
    assert res.values[2] == 8.0
    assert res.values[3] == 9.0

    assert res.index[0] == 400
    assert res.index[1] == 500
    assert res.index[2] == 600
    assert res.index[3] == 700


def test_gather():
    gth = hrsp.gather.gather('gth')

    assert len(gth) == 2
    # P=400.0 == 3.75 avg
    # P=800.0 == 7.5 avg
    for k, v in gth.items():
        if k.pressure == 400.0:
            assert v == 3.75
        elif k.pressure == 800.0:
            assert v == 7.5
        else:
            raise AssertionError
