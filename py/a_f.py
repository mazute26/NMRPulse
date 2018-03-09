#! /usr/bin/env python
"""This module contains routines to create the add_files directory tree from
the acqus file.
"""

import os
import sys
import re
import getopt
import shutil
import subprocess

# the following hack is necessary, since BRUKER does not add the directories in
#the user-defined python path to the sys.path
setup_path = '/Users/mazute26/Documents/PP_SETUP/PPlib'
if not (setup_path in sys.path):
    sys.path.append(os.path.join(setup_path, 'py'))

import ppGlobals as pp
import showJcamp as sj
import ppUtil as ut

def copy_parfile(ptype, pname, addfilecreatepath):
    """Copy individual parameter file <pname> of type <ptype> to
    <addfilecretepath>. <pname> is sought according to the Bruker search path.
    The file is copied into a subdirectory of <addfilecretepath> according to
    the relative directory in the Bruker lists directory. In case the file comes
    from outside of the lists directory (non-standard Bruker path), the file
    is put into the first subdirectory entry of lists according to the standard
    search path.
        """

    (filefullpath, defaultdir) = ut.find_file_dir(pname, ptype)
    if not filefullpath:
        ut.putcomment('<%s> not found in %s' % (pname, ptype), 0, ornament=False)
        return

    ut.putcomment('<%s> found in %s as <%s>' % (pname, ptype, filefullpath),
        1, ornament=False)

    fs = filefullpath.split(pp.lists_path + os.sep + 'lists' + os.sep)
    if len(fs) == 2:
        d = os.path.dirname(fs[1])
    else:
        ut.putcomment('<%s> found in %s with unnormal path <%s>'
            % (pname, ptype, filefullpath), 1, ornament=False)
        (dum, d) = pp.parfile_dirs_default_dict[ptype][0].split('lists' + os.sep)

    dd = os.path.join(addfilecreatepath, d)
    if not os.path.isdir(dd):
        os.makedirs(dd)

    shutil.copy2(filefullpath, os.path.join(dd, pname))


def make_add_files(u_dc, addfilecreatepath):
    """Create add_files directory into addfilecreatepath. An eventually existing
    previous directory is removed.
    The routine runs through the list of parameter names defined in
    the pp.dirs2pars_dict dictionnary. The parameter values are read out
    from the acqu file dictionnary u_dc. A list of unique parameter names and
    values is created, which are then passed individually to copy_parfile
    together with the addfilecreatpath.
    """

    if os.path.isdir(addfilecreatepath):
        shutil.rmtree(addfilecreatepath)

    arrays = u_dc['$ARRAY']

    parlist = []
    for par in pp.pars2dirs_dict.keys():
        dkey = pp.pars2dirs_dict[par][0]
        if par in arrays.keys():
            for s in u_dc[par]:
                if len(s):
                    parlist.append((dkey, s))
        else:
            parlist.append((dkey, u_dc[par]))

    parlist = sorted(set(parlist))

    for (ptype, pname) in parlist:
        copy_parfile(ptype, pname, addfilecreatepath)


def printhelp(com):
    """Create add_files directory

        usage: %s [options] [acqus filename]

        acqus filename: name of acqu(s) input file [acqus]

        [options]:
        -a      : change to current data set on Bruker instrument (uses output of command 'curd -a')
        -d name : define name of add_files directory [add_files]
        -h      : print this text
        -v num  : verbose level number [0]
        """
    print printhelp.__doc__ % com

def main():

    setopts,args = getopt.gnu_getopt(sys.argv[1:], 'ad:hv:')

    ut.cd_curd()

    pp.verbose_level = 0
    addfilesdirname = 'add_files'
    for opt in setopts:
        if opt[0] == '-h':
            printhelp(sys.argv[0])
            return
        elif opt[0] == '-a':
            cds=subprocess.Popen(["curd", "-a"], stdout=subprocess.PIPE).communicate()[0].strip()
            os.chdir(cds)
        elif opt[0] == '-d':
            addfilesdirname = opt[1]
            print addfilesdirname
        elif opt[0] == '-v':
            pp.verbose_level = 1
            pp.verbose_level = int(opt[1])

    if len(args) == 0:
        parname = 'acqus'
    else:
        parname = args[0]

    ut.putcomment('Reading Jcamp file: ' + parname, 1, ornament=True)

    if pp.verbose_level > 1:
        ut.putcomment('pp.ppGlobals', 1)
        ut.show_vars(pp)

    (j_dc, u_dc) = sj.parseJcamptxt(ut.read_file(parname))

    make_add_files(u_dc, addfilesdirname)


if __name__ == "__main__":
    main()
