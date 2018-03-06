#! /usr/bin/env python
"""
This creates a new BRUKER dataset and sets the aquisition parameters according
to the py header in the pp
"""

import os, sys, re, getopt, datetime

setup_path = '/Users/mazute26/Documents/PP_SETUP/topspinhome/PPlib'
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


def write_bruker_search_path(ftype, destfile, sourcefile=None, sourcetext=None):
    """Will copy a file from sourcefile (out of the add_files directory) or
    text to destfile in first directory of Bruker search path for
    ftype = cpd, f1, gp, ... with checks for overwrite, identity, etc.
    """
    if pp.run_flag not in pp.run_flags:
        raise Exception('unknown run_flag: ' + pp.run_flag)

    destfile = destfile + pp.name_tag
    ut.putcomment('write_bruker_search_path: start', 2)
    ut.putcomment('ftype: %s, destfile: %s' % (ftype, destfile), 2, ornament=False)
    if sourcetext and sourcefile:
        raise Exception('both sourcefile and sourcetext defined')

    if sourcetext:
        source = sourcetext
        sourcestring = 'sourcetext'
        ut.putcomment('input is from sourcetext', 2, ornament=False)
        ut.putcomment(source, 2, ornament=False)
    else:
        ut.putcomment('input is from sourcefile: ' + pp.addfiles_path + '/' + sourcefile,
            2, ornament=False)
        sourcestring = 'sourcefile <%s>' % sourcefile
        f = open(os.path.join(pp.addfiles_path,sourcefile))
        source = f.read()
        f.close()
        ut.putcomment(source, 3, ornament=False)


    (destfilefullpath, destdir) = ut.find_file_dir(destfile, ftype)
    if destfilefullpath:
        ut.putcomment('destination file exists: ' + destfilefullpath, 2, ornament=False)
        if not ut.cmp_text_file(source, destfilefullpath):
            outstring = ('PP_FILE NO_ACTION: %s equals destfile <%s>'
                %  (sourcestring, destfilefullpath))
            ut.putcomment(outstring, 1, ornament=False)
            pp.pp_log_fd.write('%s\n' % outstring)
        else:
            outstring = ('PP_FILE CONFLICT: %s is not equal to destfile <%s>'
                %  (sourcestring, destfilefullpath))
            ut.putcomment(outstring, 0, ornament=False)
            pp.pp_log_fd.write('%s\n' % outstring)
            if pp.run_flag == 'DRY':
                outstring = ('PP_FILE OVERWRITE: %s will overwrite destfile <%s>'
                    %  (sourcestring, destfilefullpath))
                pp.pp_log_fd.write('%s\n' % outstring)
            elif pp.run_flag  == 'NORMAL':
                raise Exception('%s\nPP_FILE NO_OVERWRITE: run_flag is %s\n'
                    % (outstring, pp.run_flag))
            elif pp.run_flag == 'FORCE':
                outstring = ('PP_FILE OVERWRITE: %s overwrites destfile <%s>'
                    %  (sourcestring, destfilefullpath))
                ut.putcomment(outstring, 0, ornament=False)
                pp.pp_log_fd.write('%s\n' % outstring)
                ut.write_text_file(source, destfilefullpath)
            elif pp.run_flag == 'INTERACTIVE':
                raise Exception('%s\nPP_FILE NO_OVERWRITE: run_flag is %s\n'
                % (outstring, pp.run_flag))

    else:
        df1 = os.path.join(destdir, destfile)
        outstring = ('PP_FILE CREATE: destfile <%s> from %s'
            %  (df1, sourcestring))
        ut.putcomment(outstring, 1, ornament=False)
        pp.pp_log_fd.write('%s\n' % outstring)
        if pp.run_flag == 'DRY':
            pass
        elif pp.run_flag in ['FORCE', 'NORMAL', 'INTERACTIVE']:
            ut.write_text_file(source, df1)
        else:
            raise Exception('unknown run_flag: ' + pp.run_flag)

    ut.putcomment('write_bruker_search_path: end', 2)
    return destfile


def PP_PUTPAR(name, value):
    if pp.run_flag not in pp.run_flags:
        raise Exception('unknown run_flag: ' + pp.run_flag)

    brukername = name = name.upper()
    ut.putcomment('PP_PUTPAR input: %s %s' %  (name, value), 2, ornament=False)

    m = pp.par_array_names_re.match(name)
    if m:
        ut.putcomment('detected array ' + m.group('arn') + ' ' + m.group('ind'),
            3, ornament=False)
        an = m.group('arn')
        ind = m.group('ind')

        m1 = re.match('(PL|SP)DB', an)
        if m1:
            an = m1.group(1) + 'W'
            value = pow(10.0, -value/10.)

        m1 = re.match('(D|IN|P|INP)', an)
        if m1 and (type(value) == str):
            m2 = pp.time_units_re.match(value)
            if m2:
                val = m2.group('val')
                un = m2.group('unit')
                value = float(val)*pp.time_units[un]
                if re.match('(P|INP)', an):
                            value = value * 1e6

        brukername = an + ' ' + ind

    pp.pp_log_fd.write('%s: %s\n' %  (brukername, str(value)))
    ut.putcomment('PP_PUTPAR: %s %s' %  (brukername, str(value)), ornament=False)

    if pp.run_flag == 'DRY':
        #print top.Cmd.putPar(brukername, str(value))
        return None
    elif pp.run_flag in ['FORCE', 'NORMAL', 'INTERACTIVE']:
        return TC.PUTPAR(brukername, str(value))
        return None


def PUTPARS(nams, vals):
    if (type(nams) != tuple) and (type(vals) != tuple):
        PP_PUTPAR(nams, vals)
        return
    for n,v in zip(nams, vals):
        PP_PUTPAR(n, v)

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
            #TC.NEWDATASET([expname, '1', '1', stan_dir], None, 'FHSQCF3GPPH')
            TC.NEWDATASET([expname, '1', '1', stan_dir], None, 'user/HNC_2D')
            ut.putcomment('HNC_2D used as starting parameter set.', 1,
                ornament=False)
        elif nuclei.issubset(pp.nuclei):
            TC.NEWDATASET([expname, '1', '1', stan_dir], None, 'user/HNCD')
            ut.putcomment('HNCD_2D used as starting parameter set.', 1,
                ornament=False)

    TC.RE([expname, '1', '1', stan_dir], 'y')
    ut.putcomment('New Dataset named %s created' % expname, 1, ornament=False)

def printhelp(com):
    """Set-up new Bruker data set according to Python definitions in pulse program file

    usage: %s [options] programname

    programname: name of pulse program

    [options]:
    -a      : look for programname in add_files path
    -h      : print this text
    -r flag : set run flag to <flag> (can be DRY, NORMAL, FORCE, INTERACTIVE) [DRY]
    -v num  : set verbose level number to <num> [0]
    """
    print printhelp.__doc__ % com



def main():
    ##########      GUI to choose pp file     ##########
    frame = JFrame('test')
    chooseFile = JFileChooser()
    chooseFile.setCurrentDirectory(File(pp.pp_path))

    ret = chooseFile.showOpenDialog(frame)

    if ret == JFileChooser.APPROVE_OPTION:
        file = chooseFile.getSelectedFile()
        pp1 = file.getCanonicalPath()

    pparray = pp1.split('/')
    pp_name = pparray[-1]

    ppname = pp_name
    expname = ppname.split('.')[0]
    rex = r'iPulse/(?P<exp>\w+)/\d+'
    rex = rex.replace('/', os.sep)
    match = re.search(rex, pp.addfiles_path)
    if match:
        pp.addfiles_path = pp.addfiles_path.replace(match.group('exp'), expname)
    else:
        ut.putcomment('add_files directory not found', 0, False)
    pp.pp_file =  os.path.join(pp.addfiles_path, 'pp/user/%s' %ppname)
    pp.pp_file = pp.pp_file.replace('/', os.sep)
    pplogname = ppname + '.log'
    pp.pp_log = os.path.join(pp.addfiles_path, 'pp/user/%s' %pplogname)
    pp.pp_log = pp.pp_log.replace('/', os.sep)
    ut.putcomment('Got %s from GUI' % ppname, 1, ornament=False)

    pp.verbose_level = 0
    pp.run_flag = 'DRY'

    ######      Parse input arguments   #########
    setopts,args = getopt.gnu_getopt(sys.argv[1:], 'ahr:v:')
    #
    # if len(args) == 0:
    #     printhelp(sys.argv[0])
    #     return

    for opt in setopts:
        if opt[0] == '-h':
            printhelp(sys.argv[0])
            return
        elif opt[0] == '-a':
            (pp.pp_file, adir) = ut.find_file_dir(ppname, 'PP', addfiles=True)
            if not pp.pp_file:
                raise Exception('%s not found in add_files path %s'
                    % (ppname, pp.addfiles_path))
        elif opt[0] == '-r':
            pp.run_flag = opt[1]
        elif opt[0] == '-v':
            pp.verbose_level = int(opt[1])


    ut.putcomment('Installing pulse program file: ' + pp.pp_file ,1, ornament = False)
    ut.putcomment('Logfile: %s' % os.path.abspath(pp.pp_log), 1, ornament = False)
    ut.putcomment('run_flag: %s' % pp.run_flag, 1, ornament=False)

    if pp.verbose_level > 1:
        ut.putcomment('pp.ppGlobals', 1)
        ut.show_vars(pp)

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

        ###########    Setup aquisition parameters in new Dataset     ###############

    pp.pp_log_fd = open(pp.pp_log, 'w')
    now = datetime.datetime.now()
    pp.pp_log_fd.write('Date and Time: %s \n' %now)
    exec pythontext
    pp.pp_log_fd.close()

if __name__ == "__main__":
        main()
