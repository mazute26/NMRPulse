#! /usr/bin/env python
"""
This module contains the functions to perform frequecy calculations.
"""
import os
import sys
import re
#import argparse

iupacref = {'H': 1, 'C': 0.251449530, 'N': 0.101329118, 'D': 0.153506088,
    'P': 0.404808636}
for s,d in zip(['H1','H2','C13','N15'], ['H','D','C','N']):
    iupacref[s] = iupacref[d]
spectro_wf = {'800': 800.18372587, '600nih': 600.140780, '600_0': 600.03281804,
    '600': 599.93282 }

def cs_water_T(T):
    """
    Calculates chemical shift of water based on Temparature.
    """
#   according to Gottlieb, H. E., Kotlyar, V. & Nudelman, A.
#	NMR Chemical Shifts of Common Laboratory Solvents as Trace Impurities.
#	J. Org. Chem. 62, 7512-7515 (1997).
    cs = 5.060 - 0.0122*T + (2.11e-5)*T**2
    return(cs)

def cs_water_Tp(T=298, p=1):
    """
    Calculates chemical shift of water based on Temparature and pressure (according to Maciej).
    """
#   according to Maciej
    cs = 5.945e-7*p*T  -1.612e-4*p  -1.025e-2*T  + 7.866
    return(cs)

def csWater45Me_308K_p(p=1):
    """
    Calculates chemical shift of Chemical shift of water line in 45% MeOH at 308K according to pressure (Maciej).
    """
    # Chemical shift of water line in 45% MeOH at 308K according to pressure (Maciej)
    cs = -4.324584E-05*p + 4.661946E+00
    return(cs)

def f2p_water(freqN, typeN, freqW, csw):
    """
    Converts frequecy to ppm.
    """
    fH0 = freqW /(1 +csw*1.0e-6)
    fN0 = fH0*iupacref[typeN]
    csN = (freqN/fN0 -1)*1.0e6
    return(csN)

def p2f_water(csN, typeN, freqW, csw):
    """Converts ppm to frequency."""
    fH0 = freqW /(1 +csw*1.0e-6)
    fN0 = fH0*iupacref[typeN]
    freqN = (1+csN*1.0e-6)*fN0
    return(freqN)
