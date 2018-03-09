#! /usr/bin/env python
"""
This module creates the Dataset which can be overwritten by ppSetup.
"""
import os, sys, re, getopt, datetime

setup_path = '/Users/mazute26/Documents/PP_SETUP/PPlib'
sys.path.append(os.path.join(setup_path, 'py' ))

import ppGlobals as pp
import ppUtil as ut
import ppSpect as spec
import fcalc

from javax.swing import JFrame, JFileChooser
#from java.awt import *
from java.io import File

import TopCmds as TC

stan_dir = os.path.join(os.environ['TOPO'], 'data/%s/nmr' %os.getenv("USER"))
stan_dir = stan_dir.replace('/', os.sep)

def check_if_dataset(expname, dataset_dir = stan_dir):
    """
    Goes trough dataset_dir and checks if a experiment directory named
    expname already exists.
    """
    result = os.path.isdir(os.path.join(dataset_dir, expname))
    ut.putcomment(
    'Looking for expname path: %s' % os.path.join(dataset_dir, expname),
    2, ornament=False)
    return result


def get_highest_expno(expname, dataset_dir = stan_dir):
    """
    Gets the highstes expno of a given experiment expname
    """
    directory = os.path.join(dataset_dir, expname)
    hexpno = 1
    for expno in os.listdir(directory):
        try:
               if int(expno) > int(hexpno):
                      hexpno = expno
        except ValueError:
               print 'Non interger exnpo found.'
    return str(hexpno)

class ExpType(object):
    """Class containining the type of the NMR experiment.

    Attributes:
        dim (int): Dimension of the experiment
        nuc (set): Set of used nuclei channels
    """
    def __init__(self, dimension, nuclei):
        self.dim = dimension
        self.nuc = set(nuclei)
        #Why cant that be in ppUtil for BRUKER?

def exp_type_chooser(dim, nuclei, expname):
    """Find the appropriate parameter set based on the dimension and nuclei used
    in the pulse program. This paramter set is then set as the current data set.

    Args:
        dim (int): Dimension of the pulse program
        nuclei (set): Used nuclei
        expname (str): name of the new dataset
    """
    if dim == 1:
        pass
    elif dim == 2:
        if nuclei.issubset(pp.hydrogen):
            TC.NEWDATASET([expname, '1', '1', stan_dir], None, 'standard2D')
            ut.putcomment('standard2D used as starting parameter set.', 1,
                ornament=False)
        elif nuclei.issubset((pp.hydrogen | pp.nitrogen)):
            TC.NEWDATASET([expname, '1', '1', stan_dir], None, 'HN')
            ut.putcomment('HN_2D used as starting parameter set.', 1,
                ornament=False)
        elif nuclei.issubset((pp.hydrogen | pp.carbon)):
            TC.NEWDATASET([expname, '1', '1', stan_dir], None, 'HC')
            ut.putcomment('HC_2D used as starting parameter set.', 1,
                ornament=False)
        elif nuclei.issubset((pp.hydrogen | pp.carbon | pp.nitrogen)):
            TC.NEWDATASET([expname, '1', '1', stan_dir], None, 'FHSQCF3GPPH')
            #TC.NEWDATASET([expname, '1', '1', stan_dir], None, 'user/HNC_2D')
            ut.putcomment('HNC_2D used as starting parameter set.', 1,
                ornament=False)
        elif nuclei.issubset(pp.nuclei):
            TC.NEWDATASET([expname, '1', '1', stan_dir], None, 'user/HNCD')
            ut.putcomment('HNCD_2D used as starting parameter set.', 1,
                ornament=False)

    TC.RE([expname, '1', '1', stan_dir], 'y')
    ut.putcomment('New Dataset named %s created' % expname, 1, ornament=False)

def printhelp(com):
    """Creates standard Bruker data set a or uses existing one
    according to pulse program type.

    usage: %s [options] programname

    programname: name of pulse program

    [options]:
    -h      : print this text
    -v num  : set verbose level number to <num> [0]
    """
    print printhelp.__doc__ % com



def main():
    #######    Parse arguments     #######
    setopts,args = getopt.gnu_getopt(sys.argv[1:], 'ahr:v:')

    if len(args) == 0:
        printhelp(sys.argv[0])
        return

    for opt in setopts:
        if opt[0] == '-h':
            printhelp(sys.argv[0])
            return
        elif opt[0] == '-v':
            pp.verbose_level = int(opt[1])

    ppname = args[0]
    pp.pp_file =  os.path.join(pp.addfiles_path, 'pp/user/%s' %ppname)
    expname = ppname.split('.')[0]

    pp.verbose_level = 0

    #######      Windows asking whether to use current dataset   #######
    value = TC.SELECT('Dataset', 'Set parameter in current dataset?', ['Yes', 'No'])
    if value == 0:
        ut.putcomment('Parameter are set in current dataset', 2, ornament=False)
    elif value == 1:
        ut.putcomment('Parameter are set in new dataset', 2, ornament=False)
    elif value < 0:
        raise Exception ('No dataset chosen.')

    ###########     Read pulse programm     ###############
    (pythontext, nonpythontext) = ut.split_python_text(ut.read_file(pp.pp_file))

    if not pythontext:
        raise Exception('%s contains no python text' % pp.pp_file)

    ###########     Get experiment types    ###############
    line =''
    for lines in pythontext.split('\n'):
        if 'ExpType' in lines:
            line = lines
            break
    exec line
    if pp.exp.dim not in pp.dimensions:
        raise Exception('No suitable dimension found: %d'  %pp.exp.dim)
    else:
        ut.putcomment('Dimension of the new experiment is %d.' %pp.exp.dim, 2,
            ornament=False)
    if not pp.exp.nuc.issubset(pp.nuclei):
        raise Exception('Nuclei type(s) %s not confirmed.'
            %(', '.join(pp.exp.nuc - pp.nuclei)))
    else:
        ut.putcomment(
            '%s channels are used.' %', '.join(pp.exp.nuc), 2, ornament=False)

    ###########    Create new Dataset       ###############
    if value == 1:
        expname = ppname.split('.')[0]
        datasetdir = stan_dir

        if check_if_dataset(expname):
            #Make new dataset with incremented expno
            nexpno = int(get_highest_expno(expname)) + 1
            TC.RE([expname, get_highest_expno(expname), '1', datasetdir], 'n')
            ut.putcomment('highstes expno: ' + get_highest_expno(expname), 1,
                ornament = False)
            ut.putcomment('nexpo: ' + str(nexpno), 1, ornament = False)
            TC.WR([expname, str(nexpno), '1', datasetdir], 'n')
            TC.RE([expname, str(nexpno), '1', datasetdir], 'y')
        else:
            #Make new dataset based on BRUKER standard
            exp_type_chooser(pp.exp.dim, pp.exp.nuc, expname)


if __name__ == "__main__":
    main()
