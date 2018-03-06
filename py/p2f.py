#! /usr/bin/env python

import os, sys, re
import argparse
import fcalc


def main():

    T = 298
    p = 1
    spectro='800'
    wf = spectro_wf[spectro]


    parser = argparse.ArgumentParser(description='Calculate nuclear frequency from chemical shift via water referencing')

    parser.add_argument("-wf", "--waterfrequency",  dest="waterfrequency",type=float,
                      help="water frequency in MHz ["+str(wf)+"]",
		      default=wf)

    parser.add_argument("-S", "--spectrometer", dest="waterfrequency",
                      help="name of nmr spectrometer to define water frequency "+str(spectro_wf),
                      choices = spectro_wf.keys(),
		      default=wf, action=StoreWaterFreq)

    parser.add_argument("-ws", "--watershift", dest="watershift", type=float,
                      help="water chemical shift in ppm ["+str(fcalc.cs_water_Tp(T, p))+" ("+str(T)+" K, "+str(p)+" bar)]",
		      default=fcalc.cs_water_Tp(T, p))

    parser.add_argument("-q", "--quiet",
                      action="store_false", dest="verbose", default=True)

    parser.add_argument('nuctype', metavar = 'nuctype', choices = iupacref,
    			help='type of nucleus (choose from '+str(iupacref.keys())+')')

    parser.add_argument('nucshift', metavar = 'nucshift', type=float, help='nuclear shift in ppm')

    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')

    args = parser.parse_args()

#    print args
    nucfreq = fcalc.p2f_water(args.nucshift, args.nuctype, args.waterfrequency, args.watershift)


    if args.verbose:
	print "nuctype %s nucshift %8.5f nucfreq %12.8f watershift %7.5f waterfrequency %12.8f" % (args.nuctype,
		args.nucshift, nucfreq, args.watershift, args.waterfrequency)
    else:
    	print "%12.8f" % nucfreq

if __name__ == "__main__":
    main()
