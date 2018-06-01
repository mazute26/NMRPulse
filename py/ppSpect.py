"""This module sets all the spectrometer-specific parameters, such as
frequencies, pulse powers, etc
"""
from math import log10, fabs

try:
    import matplotlib.pyplot as plt
    import numpy as np
except:
    pass

WATER_FREQUENCY = 600.13281495  # in MHz

ROUTING = {'f1': 'H', 'f2': 'N', 'f3': 'C1', 'f4': 'D'}

PULSE_POWER = {
    "C13":
        {"rect": """
10.5    -24.4
13    -22.8
15.0    -21.45
20.5    -18.85
22    -18.1
23.7    -17.55
35.0    -14.2
49    -11.15
53    -10.6
75.0    -7.5
100.0   -4.95
200    1.15
225.0   2.1
""",
         "sinc1.0": """
150    -5.8
"""},

    "N15":
        {"rect": """
40    -23.2
200    -9.2
"""},

    "H1":
        {"rect": """
6.47    -13.0
785.65    29
""",
         "sinc1.0": """
1897    26
"""},

    "H2":
        {"rect": """
93.0    -14.7
120 -12.8
"""}
}

for nuc in PULSE_POWER:
    for pulse in PULSE_POWER[nuc]:
        s = PULSE_POWER[nuc][pulse].strip().split('\n')
        pp = []
        for x in s:
            l = x.split()
            pp.append((float(l[0]), float(l[1])))
        PULSE_POWER[nuc][pulse] = sorted(pp, key=lambda tup: tup[0])


def get_pulse_power(nuc, pulse, length, nearby=False):
    """ Calculates pulse power based on spectrometer calibration set in
    dict PULSE_POWER

    Args:
        nuc: Nucleus
        pulse: pulse type
        nearby: If nearby = True then the closest value in the dict is used.
        Otherwise the pulse power is extrapolated from the closest value.

    Returns:
        A tupel (pulse length in microns, pulse power in -dBW)
    """
    pp = PULSE_POWER[nuc][pulse]
    mp = min(pp, key=lambda p: fabs(log10(length / p[0])))
    if nearby:
        return mp
    dp = 20 * log10(length / mp[0])
    ppo = mp[1] + dp
    return (length, ppo)


def plot(lin=True):
    fig = plt.figure(figsize=(12, 8), dpi=80)
    plot = fig.add_subplot(111)
    plot.set_xlabel('pulse length ['r'$\mu$s]')
    plot.set_ylabel('pulse power [-dBW]')

    logdata = []
    for length, dB in PULSE_POWER['C13']['rect']:
        logdata.append((length, dB))
    Xdata, Ydata = zip(*logdata)
    length0, dB0 = Xdata[2], Ydata[2]

    X = np.linspace(5, 240, 256, endpoint=True)
    Y = dB0 + 20 * np.log10(X / (length0))

    color = ['blue', 'orange', 'green', 'red', 'purple', 'brown', 'pink', 'gray',
             'olive', 'cyan']

    lin = 1  # lin = 1 for linear plot
    if lin:
        plot.set_xlabel('log( length ['r'$\mu$s] )')
        lindata = []
        for length, dB in PULSE_POWER['C13']['rect']:
            lindata.append((log10(length), dB))
        Xdata, Ydata = zip(*lindata)
        X = np.linspace(0, 3, 256, endpoint=True)
        Y = dB0 - 20 * np.log10(length0) + 20 * X

    plot.plot(X, Y, color=color[0], linewidth=1.0,
              linestyle='-', label='PldB1 - PldB2 = 20 log'r'$_{10}\frac{P1}{P2}$')

    plot.scatter(Xdata, Ydata, color='red', label='H.- J.  calibration')
    plot.legend(loc='upper left')
    plt.show()
    return


#####       Plot of pulse powers        #####
if __name__ == '__main__':
    plot()
