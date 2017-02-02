"""Numerical analysis of timeseries from GCMC


"""
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from statsmodels.tsa import stattools


class NotEquilibratedError(ValueError):
    pass


def check_flat(signal):
    x0, c = np.polyfit(signal.index, signal.values, 1)

    y0 = c + x0 * signal.index[0]
    y1 = c + x0 * signal.index[-1]

    totdrift = 100 * abs((y1 - y0) / signal.mean())

    if (x0 > 1e-4) and (totdrift > 5):
        raise NotEquilibratedError("Total drift was {}%".format(totdrift))
    else:
        return True


def find_equilibrium(signal):
    def split_around(sig, thresh):
        """Split *sig* around the first occurence of *thresh*

        Works on rising signals
        """
        split = sig[sig > thresh].index[0]
        return sig[:split].iloc[:-1], sig[split:]


    # rolling mean window size 
    wsize = len(signal) // 100

    half = len(signal) // 2

    back = signal.iloc[half:]

    check_flat(back)

    mean = back.mean()
    std = back.std()
    threshold = mean - 2 * std

    rm = signal.rolling(wsize, center=True).mean()

    equil, sampling = split_around(rm, threshold)

    return sampling.index[0]


def do_exp_fit(sig, thresh=0.3):
    """Fit an exponential up to thresh

    Single exponential::
      y = exp(-x/tau)

    Parameters
    ----------
    sig : pd.Series
      timeseries of the signal
    thresh : float
      value at which to cut off the signal

    Returns
    -------
    coefficient for tau
    """
    def exp_fit(x, tau):
        return np.exp(-x/tau)

    def grab_until(sig, thresh):
        """Works on falling signals"""
        # find index where signal is first below value
        cut = sig[sig < thresh].index[0]

        return sig[:cut].iloc[:-1]  # return signal up to cut, excluding cut

    sig = grab_until(sig, thresh)
    # grab sig up to where it first goes below threshhold
    
    x, y = sig.index, sig.values
    return curve_fit(exp_fit, x, y, p0=10000)[0][0]


def do_acf(signal):
    nlags = len(signal)

    acf = stattools.acf(signal, fft=True, nlags=nlags)
    # +1 as acf at zero is returned
    return pd.Series(acf, signal.index[:nlags + 1])


def find_tau(signal):
    acf = do_acf(signal)
    
    return do_exp_fit(acf)
