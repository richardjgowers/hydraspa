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
