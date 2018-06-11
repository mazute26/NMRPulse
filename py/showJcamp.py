#! /usr/bin/env python
"""Jcamp file parser
"""

import os
import sys
import re
import getopt

import ppGlobals as pp
import ppUtil as ut


# the following hack is necessary, since BRUKER does not add the directories
# in the user-defined python path to the sys.path
setup_path = '/Users/mazute26/Documents/PP_SETUP/NMRPulse'
if not (setup_path in sys.path):
    sys.path.append(os.path.join(setup_path, 'py'))

jcampstarttok = '##TITLE='
jcampendtok = '\n##END='
jcampsearchstr = r"%s(?P<jtext>.*)%s" % (jcampstarttok, jcampendtok)
jcampsearchregex = re.compile(jcampsearchstr, re.DOTALL)

jcampstringstarttok ='<'
jcampstringendtok ='>'
jcampstringsearchstr = r"%s(?P<stext>.*)%s" % (jcampstringstarttok, jcampstringendtok)
jcampstringsearchregex = re.compile(jcampstringsearchstr, re.DOTALL)

brukerarraysearchstr = r"\((?P<as>\d+)\.\.(?P<ae>\d+)\)\s+(?P<rest>.*)"
brukerarraysearchregex = re.compile(brukerarraysearchstr, re.DOTALL)


def parsevalue(val):
    try:
        val = int(val)
    except (ValueError):
        try:
            val = float(val)
        except (ValueError):
            val = str(val)
            m = jcampstringsearchregex.search(val)
            if m:
                val = m.group('stext')

    return val

def parsearray(ar, li):
    """
    Recursively parses a string ar containing a Bruker array into a list of values.
    The first value is separated from ar and parsed. The recursion restarts with
    the list li appended by the first parsed value and the remainder of ar.
    Enclosing <> are removed from strings
    Returns:
        li: list of parsed values
    """
    if len(ar) < 1:
        return li

    if ar[0] == jcampstringstarttok:
        arl = ar[1:].split(jcampstringendtok, 1)
    else:
        arl = ar.split(None, 1)

    li += [parsevalue(arl[0])]
    if len(arl) < 2:
        return li

    return parsearray(arl[1], li)

def parsebrukervalue(val):
    """
    parses the bruker value (variable name starting with $)
    decides whether it is an array
    Returns:
        (val1, ar)
        ar = (starindex, endindex) for arrays, otherwise None
        val = list of values for arrays, otherwise single value
        values are converted to int, float, or str.
        Enclosing <> are removed from strings.
    """
    m = brukerarraysearchregex.match(val)
    if m:
        ar = (int(m.group('as')),int(m.group('ae')))
        val1 = parsearray(m.group('rest'), [])
        arl = ar[1] - ar[0]
        if len(val1) != ar[1] - ar[0] +1:
            raise Exception('array length inconsistent for %s' % val)
    else:
        val1 = parsevalue(val)
        ar = None

    return (val1, ar)

def parseJcamptxt(text):
    """
    Parses Jcamp text
    Returns:
        (j_dc, u_dc)
        j_dc: dictionary of jcamp-defined variable name, value pairs
        (see McDonald, R. S.; Wilks, P. A. Appl. Spectrosc., AS 1988, 42 (1), 151.)
        u_dc: dictionary of user-defined variable name, value pairs,
        The variable names start with a $-sign, which is removed. If the value
        is an array, it is parsed using Bruker convention and returned as a list.
        The array start and end indices are stored as tuples into a
        subdictionnary $ARRAY under the array name.
    """
    j_dc = {}
    u_dc = {'$ARRAY':{}}

    m = jcampsearchregex.search(text)
    if not m:
        raise Exception('file does not contain <%s> +  <%s> tokens'
            % (jcampstarttok, jcampendtok))
    jtext = '\n' + jcampstarttok + m.group('jtext') + jcampendtok

    jtext = ut.strip_comment(jtext, '$$')
    jsplit = jtext.split('\n##')

    for jl in jsplit:
        s = jl.strip().split('=',1)
        if len(s) < 2:
            continue
        (vnam, vval) =  s
        vval = vval.strip()
        if vnam[0] != '$':
            j_dc[vnam] = parsevalue(vval)
        else:
            (val, ar) = parsebrukervalue(vval)
            u_dc[vnam[1:]] = val
            if ar:
                u_dc['$ARRAY'][vnam[1:]] = ar

    del j_dc['END']
    return (j_dc, u_dc)

def is_Jcamp(filename):
    """Return true if the given filename is a Jcamp file.
    """
    fd = open(filename, 'rb')
    chunk = fd.read(256)
    fd.close()
    if jcampstarttok in chunk: # found start token
        return True

    return False


def printJcamp(j_dc, u_dc):
    ut.putcomment('Jcamp variables', 0)
    for key in sorted(j_dc):
        print ('%s:' % key), j_dc[key]

    ut.putcomment('User variables', 0)
    arrays = u_dc['$ARRAY']
    for key in sorted(u_dc):
        if key == '$ARRAY':
            continue
        if key in arrays.keys():
            print ('%s (%d:%d):' % (key, arrays[key][0], arrays[key][1])),
            for (ii, val) in zip(range(arrays[key][0], arrays[key][1]+1), u_dc[key]):
                print ('%s(%d)' %  (val,ii)),
            print
        else:
            print ('%s:' % key), u_dc[key]

def printarraylist(u_dc):
    arrays = u_dc['$ARRAY']

    ut.putcomment('User variable arrays', 0)
    for key in sorted(arrays):
        print ('%s:' % key), arrays[key]

def printpar(par, u_dc):
    pars = par.split()
    key = pars[0]
    arrays = u_dc['$ARRAY']
    if key in arrays.keys():
        if len(pars) < 2:
            print ('%s (%d:%d):' % (key, arrays[key][0], arrays[key][1])),
            for (ii, val) in zip(range(arrays[key][0], arrays[key][1]+1), u_dc[key]):
                print ('%s(%d)' %  (val,ii)),
            print
        else:
            ind = int(pars[1])
            print ('%s %d: %s' % (key, ind, u_dc[key][ind]))
    else:
        print ('%s: %s' % (key, u_dc[key]))



def printhelp(com):
    """Show content of Jcamp file

    usage: %s [options] JcampName [parlist]

    JcampName: name of Jcamp input file

    [parlist]: comma-separated list of parameters: par_1, par_2, ... If not given, all parameters are listed
        only applies to user-defined parameters in Jcamp file
        par_i: single_parameter_name | parameter_array_name | parameter_array_name array_index

    [options]:
    -a     : print only user array names and indices
    -h     : print this text
    -v num : verbose level number
"""
    print printhelp.__doc__ % com

def main():

    setopts,args = getopt.gnu_getopt(sys.argv[1:], 'ahv:')

    ut.cd_curd()

    if len(args) == 0:
        printhelp(sys.argv[0])
        return

    pp.verbose_level = 0
    printarraylistflag = False
    for opt in setopts:
        if opt[0] == '-h':
            printhelp(sys.argv[0])
            return
        elif opt[0] == '-a':
            printarraylistflag = True
        elif opt[0] == '-v':
            pp.verbose_level = int(opt[1])

    parname = args[0]

    ut.putcomment('Reading Jcamp file: ' + parname, 1, ornament=False)

    if pp.verbose_level > 1:
        ut.putcomment('pp.ppGlobals', 1)
        ut.show_vars(pp)

    (j_dc, u_dc) = parseJcamptxt(ut.read_file(parname))

    if printarraylistflag:
        printarraylist(u_dc)
        return

    if len(args) == 1:
        printJcamp(j_dc, u_dc)
        return

    if len(args) > 1:
        parlist = reduce(lambda x,y: x + ' ' + y, args[1:]).split(',')
        for par in parlist:
            printpar(par, u_dc)
        return



if __name__ == "__main__":
    main()
