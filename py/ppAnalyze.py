#! /usr/bin/env python
"""This module contains routines to analyse existing pulse programs together
with their acquisition data files to make suggestions for programming the used
parameters in the python header of the new pulse programs.
"""

import os
import sys
import re
import getopt
from optparse import OptionParser

import .ppGlobals as pp
import .showJcamp as sj
import .ppUtil as ut

# the following hack is necessary, since BRUKER does not add the directories
#in the user-defined python path to the sys.path
setup_path = '/Users/mazute26/Documents/PP_SETUP/PPlib'
if not (setup_path in sys.path):
    sys.path.append(os.path.join(setup_path, 'py'))


def analyzepp(progfilename, parfilename):
    """Analyze pulse program <progfilename> using acqu file <parfilename>.
    Outputs the acquisition parameters and their value.
    """

    (pythontext, nonpythontext) = ut.split_python_text(ut.read_file(progfilename))
    nonpythontext = ut.strip_comment(nonpythontext, ';')

    (j_dc, u_dc) = sj.parseJcamptxt(ut.read_file(parfilename))
    arrays = u_dc['$ARRAY']

    usedpars = []
    usedpararrays = {}
    words = sorted(set(re.split('\W+', nonpythontext)))
    ut.putcomment('parsing <%s>' % os.path.basename(progfilename), 1)
    for w in words:
        m = pp.search_commands_re.match(w)
        if m:
            if m.group('comarray'):
                c = m.group('comarray').upper()
                ind = int(m.group('ind'))
                p = pp.coms2pars_dict[c][0]
                usedpars += [p]
                ut.putcomment('%s: %s %d' % (w, pp.coms2pars_dict[c], ind), 1, ornament=False)
                if not p in usedpararrays.keys():
                    usedpararrays[p] = [ind]
                else:
                    usedpararrays[p] += [ind]
            elif m.group('com'):
                c = m.group('com').upper()
                p = pp.coms2pars_dict[c][0]
                ut.putcomment('%s: %s' % (w, pp.coms2pars_dict[c]), 1, ornament=False)
                usedpars += [p]
    ut.putcomment('end parsing', 1)


    usedpars = sorted(set(usedpars))
    for par in usedpars:
        conpars = pp.coms2pars_dict[pp.pars2coms_dict[par][0]]
        if par in pp.par_array_names:
            for ind in sorted(usedpararrays[par]):
                for p in conpars:
                    print ('%s %d: %s' % (p, ind, u_dc[p][ind]))
        else:
            for p in conpars:
                print ('%s: %s' % (p, u_dc[p]))


def main():

    usage = """usage: %prog [options] programname

Analyze pulse program file <programname> to make suggestions for automated set-up"""


    parser = OptionParser(usage)
    parser.add_option("-a", "--add_files", action="store_true", dest="addfiles", default=False,
        help="look for <programname> in add_files path [default: %default]")
    parser.add_option("-v", "--verboselevel", type="int", default = 0, dest="verboselevel",
        help="set verbose level [default: %default]")

    (options, args) = parser.parse_args()
    ut.cd_curd()

#    print options

    if len(args) == 0:
        parser.error("incorrect number of arguments")
        return

    ppname = args[0]
    pp.pp_file = os.path.abspath(ppname)

    pp.verbose_level = options.verboselevel

    if options.addfiles:
        (pp.pp_file, adir) = ut.find_file_dir(ppname, 'PP', addfiles=True)
        if not pp.pp_file:
            raise Exception('%s not found in add_files path %s' % (ppname, pp.addfiles_path))

    ut.putcomment('Analyzing pulse program file: ' + pp.pp_file ,1, ornament = False)

    if pp.verbose_level > 1:
        ut.putcomment('pp.ppGlobals', 1)
        ut.show_vars(pp)

    parfilename = 'acqus'

    analyzepp(pp.pp_file, parfilename)

if __name__ == "__main__":
    main()
