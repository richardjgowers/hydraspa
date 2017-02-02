"""Numerical analysis of timeseries from GCMC


"""


def split_around(sig, thresh):
    """Split *sig* around the first occurence of *thresh*

    Works on rising signals
    """
    split = sig[sig > thresh].index[0]
    
    return sig[:split].iloc[:-1], sig[split:]


def check_flat(signal):
    # todo: check that this signal is flat
    pass


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
