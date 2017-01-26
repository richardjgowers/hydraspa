import numpy as np
import pytest

import paraspa as prsp

# known data from the files
SERIES1 = [0.0, 1.5, 3.5, 10.0]
SERIES2 = [0.0, 2.2, 4.4, 6.6]

@pytest.fixture
def gather_results():
    return prsp.gather('gth')


class TestGather(object):
    def test_return_types(self, gather_results):
        assert isinstance(gather_results, dict)
        for thing in gather_results.values():
            assert isinstance(thing, np.ndarray)
    
    def test_found_dirs(self, gather_results):
        assert 'gth_part_1' in gather_results
        assert 'gth_part_2' in gather_results
        
    def test_parsed_values(self, gather_results):
        assert all(gather_results['gth_part_1'] == SERIES1)
        assert all(gather_results['gth_part_2'] == SERIES2)
