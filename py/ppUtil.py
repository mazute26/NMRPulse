"""This module contains utility routines for the pp project.
"""


import os
import sys
import re
import math as m

import ppGlobals as pp

try:
    import TopCmds as TC
except:
    pass


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
        la[idx] = l.split(commentid,1)[0]
    return reduce( lambda x,y: x + '\n' + y, la)


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
    fh =  open(file)
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
    '''
    Find file <filename> in search path defined in
    pp.parfile_dirs_dict (addfiles=False) or
    pp.parfile_dirs_default_dict (addfiles=True) under the key <dirs_type>.
    Returns:
        (filepath, dirpath)
    filepath: absolute path to file name if file exists (else None)
    dirpath: absolute path to first directory in search path to write
    new file
    '''
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
            pdc = par_dc_dir.split('lists'+os.sep,1)
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
        s = s +  '%8.1f\n' % ((f-fo)*1e6)
    return s

def cd_curd():
    """Check whether this is in topspin environment.
    In this case, change to current data set. Else do nothing.
    """
    if not ('TopCmds' in sys.modules):
        return
    cd = TC.CURDATA()
    os.chdir(os.path.join(cd[3], cd[0], cd[1])) #Topspin dataset path:
                                                #expname/expnumber/processnumber

def putcomment(comment, verbosethreshold = 1, ornament=True):
    """Print comment if above the verbose threshold
    with ornament (ornament = True)
    """
    if pp.verbose_level < verbosethreshold:
        return
    cs = '###################'
    ss = '   '
    if ornament:
        print '\n' +cs +ss +comment +ss + cs +'\n'
    else:
        print comment
    return

# class ExpType(object):
#     """Class containining the type of the NMR experiment.
#
#     Attributes:
#         dim (int): Dimension of the experiment
#         nuc (set): Set of used nuclei channels
#     """
#     def __init__(self, dimension, nuclei):
#         self.dim = dimension
#         self.nuc = set(nuclei)
