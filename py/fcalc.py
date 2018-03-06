#! /usr/bin/env python

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
#   according to Gottlieb, H. E., Kotlyar, V. & Nudelman, A.
#	NMR Chemical Shifts of Common Laboratory Solvents as Trace Impurities.
#	J. Org. Chem. 62, 7512-7515 (1997).
	cs = 5.060 - 0.0122*T + (2.11e-5)*T**2
	return(cs)

def cs_water_Tp(T=298, p=1):
#   according to Maciej
	cs = 5.945e-7*p*T  -1.612e-4*p  -1.025e-2*T  + 7.866
	return(cs)

def csWater45Me_308K_p(p=1):
	# Chemical shift of water line in 45% MeOH at 308K according to pressure (Maciej)
	cs = -4.324584E-05*p + 4.661946E+00
	return(cs)

def f2p_water(freqN, typeN, freqW, csw):
	fH0 = freqW /(1 +csw*1.0e-6)
	fN0 = fH0*iupacref[typeN]
	csN = (freqN/fN0 -1)*1.0e6
	return(csN)

def p2f_water(csN, typeN, freqW, csw):
	fH0 = freqW /(1 +csw*1.0e-6)
	fN0 = fH0*iupacref[typeN]
	freqN = (1+csN*1.0e-6)*fN0
	return(freqN)


#class StoreWaterFreq(argparse.Action):
#	def __call__(self, parser, namespace, values, option_string=None):
#		print 'before %r %r %r' % (namespace, values, option_string)
#		setattr(namespace, self.dest, spectro_wf[values])
#		print 'after %r %r %r' % (namespace, values, option_string)


#def main():


#    T = 298
#    p = 1
#    spectro='800'
#    wf = spectro_wf[spectro]


#    parser = argparse.ArgumentParser(description='Calculate chemical shift from nuclear frequency via water referencing')

#    parser.add_argument("-wf", "--waterfrequency",  dest="waterfrequency",type=float,
#                      help="water frequency in MHz ["+str(wf)+"]",
#		      default=wf)

#    parser.add_argument("-S", "--spectrometer", dest="waterfrequency",
#                      help="name of nmr spectrometer to define water frequency "+str(spectro_wf),
#                      choices = spectro_wf.keys(),
#		      default=wf, action=StoreWaterFreq)

#    parser.add_argument("-ws", "--watershift", dest="watershift", type=float,
#                      help="water chemical shift in ppm ["+str(fcalc.cs_water_Tp(T, p))+" ("+str(T)+" K, "+str(p)+" bar)]",
#		      default=fcalc.cs_water_Tp(T, p))

#    parser.add_argument("-q", "--quiet",
#                      action="store_false", dest="verbose", default=True)
#
#    parser.add_argument('nuctype', metavar = 'nuctype', choices = iupacref,
#    			help='type of nucleus (choose from '+str(iupacref.keys())+')')

#    parser.add_argument('nucfreq', metavar = 'nucfreq', type=float, help='nuclear frequency in MHz')
#
#    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')

#    args = parser.parse_args()

#    print args
#    nucshift = f2p_water(args.nucfreq, args.nuctype, args.waterfrequency, args.watershift)


#    if args.verbose:
#	print "nuctype %s nucshift %8.5f nucfreq %12.8f watershift %7.5f waterfrequency %12.8f" % (args.nuctype,
#		nucshift, args.nucfreq, args.watershift, args.waterfrequency)
#    else:
#    	print "%8.5f" % nucshift

#if __name__ == "__main__":
#	main()
#    import os, sys, re
#    import argparse

#    class StoreWaterFreq(argparse.Action):
#	def __call__(self, parser, namespace, values, option_string=None):
#		print 'before %r %r %r' % (namespace, values, option_string)
#		setattr(namespace, self.dest, spectro_wf[values])
#		print 'after %r %r %r' % (namespace, values, option_string)

#main()
