from __future__ import division

import numpy as np
import pandas as pd
import pytest

from hydraspa import analyse


def gen_sig(eq, prod, endval):
    """Generate a signal which rises to an equilibrium value

    Parameters
    ----------
    eq
      length of equilibrium period
    prod
      length of production period
    endval
      final mean value of signal

    Returns
    -------
    Pandas series

    Signal will oscillate as a sine wave during production
    """
    m = (endval - 1) / eq

    eq_sig = np.arange(eq) * m
    prod_sig = - np.cos(np.linspace(0, 100, prod)) + endval

    total = np.arange(eq + prod)
    signal = np.concatenate([eq_sig, prod_sig])

    return pd.Series(signal, total)


def gen_sig_with_drift(eq, prod, endval, drift):
    """Generate a signal, which drifts once reaching production

    Parameters
    ----------
    eq, prod, endval
      See gen_sig
    drift
      The total % drift during the production phase
    """
    sig = gen_sig(eq, prod, endval)

    drift = np.linspace(0, 1, prod) * endval * (drift / 100.)

    sig.iloc[eq:] += drift

    return sig


def gen_tau_signal(tau, length):
    """Generate an oscillating signal with period tau

    Parameters
    ----------
    tau
      time period of oscillations
    length
      in units of tau, total length of signal.  Returned signal
      will be of length (tau * length)
    """
    final_length = tau * length
    # length in multiples of tau
    
    min_tau = 0.9 * tau
    max_tau = 1.1 * tau
    
    pieces = [np.sin(np.linspace(0, np.pi, t))
             for t in np.linspace(min_tau, max_tau, 50, dtype=np.int)]

    tlen = 0
    tsig = []
    while tlen < final_length:
        p = np.random.choice(pieces) * np.random.choice([1, -1])
        tsig.append(p)
        tlen += len(p)
    signal = np.concatenate(tsig)
    signal = signal[:final_length]
    signal += (np.random.random(final_length) - 0.5) * 0.5

    return pd.Series(signal, np.arange(final_length))


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


class TestFindTau(object):
    @pytest.mark.parametrize('tau', [100, 200, 500])
    @pytest.mark.parametrize('length', [150, 300, 500])
    def test_tau(self, tau, length):
        sig = gen_tau_signal(tau, length)

        exp = 0.6 * tau

        assert analyse.find_tau(sig) == pytest.approx(exp, rel=0.05)
