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


def gen_sig_with_drift(eq, prod, endval, drift):
    sig = gen_sig(eq, prod, endval)

    drift = np.linspace(0, 1, prod) * endval * (drift / 100.)

    sig.iloc[eq:] += drift

    return sig


class TestFindEQ(object):
    @pytest.mark.parametrize('eq', [1000, 2000, 3000])
    @pytest.mark.parametrize('prod', [3000, 4000, 5000, 6000])
    @pytest.mark.parametrize('endval', [10, 50, 100])
    def test_find_eq(self, eq, prod, endval):
        sig = gen_sig(eq, prod, endval)

        est_eq = analyse.find_equilibrium(sig)

        # 5% tolerance allowed
        assert est_eq == pytest.approx(eq, rel=0.05)

    @pytest.mark.parametrize('eq', [1000, 2000, 3000])
    @pytest.mark.parametrize('prod', [300, 400, 500])
    @pytest.mark.parametrize('endval', [10, 50, 100])
    def test_not_equilibrated_smallprod(self, eq, prod, endval):
        sig = gen_sig(eq, prod, endval)

        with pytest.raises(analyse.NotEquilibratedError):
            analyse.find_equilibrium(sig)

    @pytest.mark.parametrize('endval', [10, 50, 100])
    @pytest.mark.parametrize('drift', [7, 10])
    def test_not_equilibrated_drift(self, endval, drift):
        sig = gen_sig_with_drift(2000, 2000, endval, drift)

        with pytest.raises(analyse.NotEquilibratedError):
            analyse.find_equilibrium(sig)
        
    @pytest.mark.parametrize('endval', [10, 50, 100])
    @pytest.mark.parametrize('drift', [1, 3])
    def test_allowed_drift(self, endval, drift):
        sig = gen_sig_with_drift(2000, 2000, endval, drift)

        assert analyse.find_equilibrium(sig) == pytest.approx(2000, rel=0.05)
