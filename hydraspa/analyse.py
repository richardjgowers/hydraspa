"""Numerical analysis of timeseries from GCMC


"""
import numpy as np


class NotEquilibratedError(ValueError):
    pass


def split_around(sig, thresh):
    """Split *sig* around the first occurence of *thresh*

    Works on rising signals
    """
    split = sig[sig > thresh].index[0]
    
    return sig[:split].iloc[:-1], sig[split:]


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


def find_tau(signal):
    pass
