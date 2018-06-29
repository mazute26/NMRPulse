#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains all the globals for NMRPulse.
It contains mostly Bruker parameter definitions and paths.
"""

import os
import re

verbose_level = 0
run_flag = 'DRY'
run_flags = ['DRY', 'NORMAL', 'INTERACTIVE', 'FORCE']

topspin_home = '/Users/mazute26/Documents/PP_SETUP/topspinhome'
setup_path = '/Users/mazute26/Documents/PP_SETUP/NMRPulse'

input_path = os.path.abspath(setup_path)
input_path = input_path.replace('/', os.sep)
addfiles_path = os.path.abspath(os.path.join(
    setup_path, 'Library/calibh/1/add_files'))
addfiles_path = addfiles_path.replace('/', os.sep)

# For Local Bruker Path PPlib
lists_path = os.path.join(topspin_home, 'exp/stan/nmr')
lists_path = lists_path.replace('/', os.sep)
userhome_dot_topspin = os.path.join(topspin_home, 'classes')
userhome_dot_topspin = userhome_dot_topspin.replace('/', os.sep)
library_path = os.path.join(setup_path, 'Library')
library_path = library_path.replace('/', os.sep)

parfile_dirs_prop_default_path = os.path.join(
    topspin_home, 'classes/prop/parfile-dirs.prop')
parfile_dirs_prop_default_path = parfile_dirs_prop_default_path.replace('/', os.sep)
parfile_dirs_prop_path = os.path.join(
    userhome_dot_topspin, 'prop/parfile-dirs.prop')
parfile_dirs_prop_path = parfile_dirs_prop_path.replace('/', os.sep)
if not os.path.isfile(parfile_dirs_prop_path):
    parfile_dirs_prop_path = parfile_dirs_prop_default_path


def read_parfile_dirs_props(filename):
    """Reads BRUKER parfile-dirs.prop file to in order to get correct mapping
        of the topspin parameters.

    Args:
        filename: input Bruker parfile-dirs.prop file

    Returns:
        A dict mapping parameter classes to the their respective directory.
        E.g. {'PY_DIRS': ['py/user', 'py']}
    """

    fh = open(filename)
    dirs = fh.read()
    fh.close()

    par_dc = {}
    dirs = dirs.replace('\\\n', '').replace(';', ' ')
    for line in dirs.split('\n'):
        if len(line) > 0 and line[0] != '#':
            key, values = line.split('=')
            par_dc[key] = values.split()

    if verbose_level > 1:
        print 'Dictionary for BRUKER search paths:'
        for key in par_dc.keys():
            print key, par_dc[key]

    return par_dc


parfile_dirs_dict = read_parfile_dirs_props(parfile_dirs_prop_path)
parfile_dirs_default_dict = read_parfile_dirs_props(
    parfile_dirs_prop_default_path)


def many2many_dicts(m2mlist):
    """
    Maps objects from one list to the other list and vice versa.

    Args:
        m2mlist: list of 2lists [list1i, list2i] where list1i, list2i represent
        a many to many mapping
    Returns:
        (one2two, two2one) : one2two, two2one
        dictionaries from elements of list1i to list2i and vice versa
    """
    one2two = {}
    two2one = {}
    for one, two in m2mlist:
        for k in one:
            one2two[k] = two
            for k in two:
                two2one[k] = one
    return (one2two, two2one)


dirs_pars = [
    [['CPD_DIRS'], ['CPDPRG']],
    [['F1_DIRS'], ['FQ%dLIST' % x for x in range(1, 9)]],
    [['GP_DIRS'], ['GPNAM', 'GRDPROG']],
    [['PP_DIRS'], ['PULPROG']],
    [['SHAPE_DIRS'], ['SPNAM']],
    [['VC_DIRS'], ['VCLIST']],
    [['VD_DIRS'], ['VDLIST']],
    [['VP_DIRS'], ['VPLIST']],
    [['VT_DIRS'], ['VTLIST']]
]
(dirs2pars_dict, pars2dirs_dict) = many2many_dicts(dirs_pars)

pp_file = None
pp_log = None
pp_log_fd = None
name_tag = ''

par_array_names = ['AMP', 'AMPCOIL', 'CAGPARS', 'CNST', 'CPDPRG', 'D',
                   'FCUCHAN', 'FS', 'GPNAM', 'GPX', 'GPY', 'GPZ', 'HGAIN', 'HPMOD', 'IN',
                   'INF', 'INP', 'L', 'MULEXPNO', 'P', 'PACOIL', 'PCPD', 'PEXSEL', 'PHCOR',
                   'PL', 'PLW', 'PLWMAX', 'PRECHAN', 'RECCHAN', 'RECPRE', 'RECPRFX', 'RECSEL',
                   'ROUTWD1', 'ROUTWD2', 'RSEL', 'S', 'SELREC', 'SP', 'SPNAM', 'SPOAL',
                   'SPOFFS', 'SPPEX', 'SPW', 'SUBNAM', 'SWIBOX', 'TE_STAB', 'TL', 'XGAIN']
par_array_names += ['PLDB', 'SPDB']  # note 'PLDB', 'SPDB' do not exist in aqcu, added by SG
rex = reduce(lambda x, y: x + '|' + y, par_array_names)
rex = '(?P<arn>' + rex + ')\s*(?P<ind>\d+)'
par_array_names_re = re.compile(rex)

time_units = {'s': 1e0, 'm': 1e-3, 'u': 1e-6, 'n': 1e-9}
rex = reduce(lambda x, y: x + '|' + y, time_units.keys())
rex = '(?P<val>[0-9.]+)\s*(?P<unit>' + rex + ')'
time_units_re = re.compile(rex)

coms_pars = [
    [['CPD', 'CPDS'], ['CPDPRG']],
    [['P'], ['P']],
    [['PL'], ['PLW']],
    [['SP'], ['SPNAM', 'SPOFFS', 'SPW']],
    [['GP'], ['GPNAM', 'GPX', 'GPY', 'GPZ']],
    [['ID', 'DD'], ['IN']],
    [['INP'], ['INP']],
    [['L'], ['L']],
    [['IVC'], ['VCLIST']],
    [['IVD'], ['VDLIST']]
]
coms_pars += [[['FQ%d' % x], ['FQ%dLIST' % x]] for x in range(1, 9)]

(coms2pars_dict, pars2coms_dict) = many2many_dicts(coms_pars)

arrcoms = []
narrcoms = []
for a in coms2pars_dict.keys():
    if coms2pars_dict[a][0] in par_array_names:
        arrcoms.append(a)
    else:
        narrcoms.append(a)

rex1 = reduce(lambda x, y: x + '|' + y, arrcoms)
rex2 = reduce(lambda x, y: x + '|' + y, narrcoms)

rex = '(?P<comarray>' + rex1 + ')(?P<ind>[0-9]+)|(?P<com>' + rex2 + ')'
search_commands_re = re.compile(rex, re.IGNORECASE)

del [a, x, arrcoms, narrcoms, rex, rex1, rex2]

exp = None
dimensions = set([1, 2])
hydrogen = set(['H', '1H', 'H1'])
nitrogen = set(['N', '15N', 'N15'])
carbon = set(['C', '13C', 'C13'])
deuterium = set(['D', '2H', 'H2'])
nuclei = hydrogen | nitrogen | carbon | deuterium
