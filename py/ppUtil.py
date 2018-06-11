"""This module contains utility routines for the pp project.
"""

import os
import sys
import re
import math as m
import .ppGlobals as pp
import .ppSpect as spec

try:
    import TopCmds as TC
except ImportError:
    print 'TopCmds.py not found'

setup_path = '/Users/mazute26/Documents/PP_SETUP/NMRPulse'
sys.path.append(os.path.join(setup_path, 'py'))


def merge_dicts(*dict_args):
    """
        Given any number of dicts, shallow copy and merge into a new dict,
        precedence goes to key value pairs in later dicts:
        z = merge_dicts(a, b, c, d, e, f, g)
        i.e. key value pairs in g will take precedence over dicts a to f,
        and so on.
    """

    result = {}
    for dictionary in dict_args:
        result.update(dictionary)

    return result


def strip_comment(text, commentid):
    """strips all text from lines in text after commentid
    """
    la = text.splitlines()
    for idx, l in enumerate(la):
        la[idx] = l.split(commentid, 1)[0]
    return reduce(lambda x, y: x + '\n' + y, la)


def show_vars(scope):
    """shows variables in scope
    """
    gs = [g for g in dir(scope) if not g.startswith('__')]
    for g in gs:
        print g, vars(scope)[g]


def read_file(file):
    """reads file
    """
    fh = open(file)
    data = fh.read()
    fh.close()
    return data


def write_text_file(text, file):
    """(over)writes text to file
    """
    fh = open(file, 'w')
    fh.write(text)
    fh.close()


def cmp_text_file(text, file):
    """returns True when text and file content are identical
    """
    fh = open(file)
    ftext = fh.read()
    fh.close()
    return cmp(ftext, text)


def split_python_text(text):
    """
    splits first '#ifdef PYTHON_SETUP ... #endif python section from text
    Returns:
        (pythontext, nonpythontext)
    """
    s = text.split('#ifdef PYTHON_SETUP', 1)
    if len(s) < 2:
        return (None, text)

    (beforep, afterp) = s
    (pythontext, aftere) = afterp.split('\n#endif', 1)
    nonpythontext = beforep + aftere
    return (pythontext, nonpythontext)


def find_file_dir(filename, dirs_type, addfiles=False):
    """
    Find file <filename> in search path defined in
    pp.parfile_dirs_dict (addfiles=False) or
    pp.parfile_dirs_default_dict (addfiles=True) under the key <dirs_type>.
    Returns:
        (filepath, dirpath)
    filepath: absolute path to file name if file exists (else None)
    dirpath: absolute path to first directory in search path to write
    new file
    """
    dte = dirs_type.upper()
    if not re.search('_DIRS$', dte):
        dte += '_DIRS'

    cwd = os.getcwd()
    if not addfiles:
        os.chdir(pp.lists_path)
        pdict = pp.parfile_dirs_dict
    else:
        os.chdir(pp.addfiles_path)
        pdict = pp.parfile_dirs_default_dict

    filepath = None

    for par_dc_dir in pdict[dte]:
        if addfiles:
            pdc = par_dc_dir.split('lists' + os.sep, 1)
            if len(pdc) < 2:
                raise Exception('%s not in add_files directory' % par_dc_dir)
            par_dc_dir = pdc[1]

        fp1 = os.path.join(par_dc_dir, filename)
        if os.path.isfile(fp1):
            filepath = os.path.abspath(fp1)
            break

    dirpath = os.path.abspath(pdict[dte][0])

    os.chdir(cwd)
    return (filepath, dirpath)


def flist_to_Bruker_flist(fs):
    """Converts frequency list to Bruker frequency list
    Args:
        fs: List with frequencies in MHz
    Return:
        s: Bruker compatible frequency list.
    """
    fo = m.floor(fs[1])
    s = 'O %5.1f\n' % fo
    for f in fs:
        s = s + '%8.1f\n' % ((f - fo) * 1e6)
    return s


def cd_curd():
    """Check whether this is in topspin environment.
    In this case, change to current data set. Else do nothing.
    """
    if not ('TopCmds' in sys.modules):
        return
    cd = TC.CURDATA()
    os.chdir(os.path.join(cd[3], cd[0], cd[1]))  # Topspin dataset path:
    # expname/expnumber/processnumber


def putcomment(comment, verbosethreshold=1, ornament=True):
    """Print comment if above the verbose threshold
    with ornament (ornament = True)
    """
    if pp.verbose_level < verbosethreshold:
        return
    cs = '###################'
    ss = '   '
    if ornament:
        print '\n' + cs + ss + comment + ss + cs + '\n'
    else:
        print comment
    return


def checkSer():
    [expdir, expnum, procnum, userdir] = TC.CURDATA()
    isSer = os.path.isfile('%s/%s/%s/ser' % (userdir, expdir, expnum))
    isFid = os.path.isfile('%s/%s/%s/fid' % (userdir, expdir, expnum))

    if isSer or isFid:
        warning = TC.SELECT('', 'This experiment number contains data',
                            ['DONT OVERWRITE', 'OVERWRITE'])
        print warning
        if warning is not None:
            if warning == 0:
                TC.EXIT()
        else:
            TC.EXIT()


def load_templt(templt, expname, stan_dir):
    # checkSer()
    try:
        TC.NEWDATASET([expname, '1', '1', stan_dir])
        TC.RE([expname, '1', '1', stan_dir], 'y')
        TC.XCMD('rpar %s all' % templt)
    except:
        TC.MSG('''You need to define the parameter set "%s" defining the correct
    routing to continue.
    First define the correct routing using edasp.
    Then save the parmeterset using:
    wpar %s all
    ''' % (templt, templt))
        TC.EXIT()


def bits_overwrite(bits):
    """Overwrites the channel definitions in bits.sg
        bits: path to bits.sg file
    """
    lines2 = []
    fh = open(bits, 'r')
    lines = fh.readlines()
    for line in lines:
        for channel in spec.ROUTING:
            rex = r'#define *(?P<nuc>\w+) *(?P<channel> %s)' %channel
            match =re.search(rex, line)
            if match:
                line = line.replace(match.group('nuc'), spec.ROUTING[channel])
        lines2.append(line)

    fh.close()
    fh = open(bits, 'w')
    fh.writelines(lines2)
    fh.close()
    return


class ExpType(object):
    """Class containining the type of the NMR experiment.

    Attributes:
        dim (int): Dimension of the experiment
        nuc (set): Set of used nuclei channels
    """

    def __init__(self, dimension, nuclei):
        self.dim = dimension
        self.nuc = set(nuclei)
