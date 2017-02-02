from __future__ import division

import numpy as np
import pandas as pd
import pytest

from hydraspa import analyse


def gen_sig(eq, prod, endval):
    m = (endval - 1) / eq

    eq_sig = np.arange(eq) * m
    prod_sig = - np.cos(np.linspace(0, 100, prod)) + endval

    total = np.arange(eq + prod)
    signal = np.concatenate([eq_sig, prod_sig])

    return pd.Series(signal, total)


class TestFindEQ(object):
    @pytest.mark.parametrize('eq', [1000, 2000, 3000])
    @pytest.mark.parametrize('prod', [3000, 4000, 5000, 6000])
    @pytest.mark.parametrize('endval', [10, 50, 100])
    def test_find_eq(self, eq, prod, endval):
        sig = gen_sig(eq, prod, endval)

        est_eq = analyse.find_equilibrium(sig)

        # 5% tolerance allowed
        assert est_eq == pytest.approx(eq, rel=0.05)
