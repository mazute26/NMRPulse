#! /usr/bin/env python
"""This macro is used to setup the PPlib project. It should be located besides the
topspin directory.
"""

import os
import shutil
import sys
import re
import readline

fpath = os.path.realpath(__file__)
PPlib = fpath.rsplit(os.sep, 1)[0]
version = '3.2pl7'
# top = os.path.join(fpath.rsplit(os.sep, 3)[0], 'topspin%s' %version)
topo = os.path.join(fpath.rsplit(os.sep, 3)[0], 'topspin')

mess = """
    Please enter the topspin directory:
    e.g. %s

    """ % fpath.rsplit(os.sep, 2)[0]
var = raw_input(mess)

top = var


def set_path(pyfile, dirname, path):
    """Changes the lines in the file, which contain a directory path definition.
    Args:
        pyfile (str): py file containing the definition
        e.g. setup_path = '/Users/username/Documents/iPulse'
        dirname (str): directory name that should be set
        e.g. setup_path
        path (str): New path that should be set
    """
    newline = []
    f = open(pyfile)
    lines = f.readlines()
    rex = r'%s *= *(?P<path>.+)' % dirname
    for line in lines:
        match = re.search(rex, line)
        if match:
            newline.append(line.replace(match.group('path'), '\'%s\'' % path))
        else:
            newline.append(line)
    f.close()
    fh = open(pyfile, 'w')
    fh.writelines(newline)
    fh.close()
    return None


set_path(os.path.join(PPlib, 'py%sppGlobals.py' % os.sep), 'topspin_home', top)
set_path(os.path.join(PPlib, 'py%sppGlobals.py' % os.sep), 'setup_path', PPlib)
for files in os.listdir(os.path.join(PPlib, 'py')):
    if files.endswith('.py'):
        set_path(os.path.join(PPlib, 'py%s%s' % (os.sep, files)), 'setup_path', PPlib)

mess = """
    %s  is used as tospin home directory.
    %s  is used as PPlib directory.
    """ % (top, PPlib)
print mess
#
# #Change Python path in parfile
# parfile = os.path.join(top, 'classes/prop/parfile-dirs.prop')
# parfile = os.path.abspath(parfile)
# parfile = parfile.replace('/', os.sep)
#
# lines2 = []
# if os.path.isfile(parfile):
#     fh = open(parfile)
#     lines = fh.readlines()
#     for line in lines:
#         if 'PY_DIRS' in line[:len('PY_DIRS')]:
#             line = line.replace('PY_DIRS=', 'PY_DIRS=%s/py;\\\r' %PPlib)
#             lines2.append(line)
#         else:
#             lines2.append(line)
#     fh.close()
#
#     i=0
#     while os.path.isfile('%s%d' % (parfile,i)):
#         i+=1
#     os.rename(parfile,'%s%d' % (parfile,i))
#
#     fh=open(parfile,'w')
#     fh.writelines(lines2)
#     fh.close()
#
#     mess='''
#     ###################           ###################
#         The parfile has been modified.
#         The previous preferences are backup in the following file:
#         %s%d
#         ''' % (parfile,i)
#     print mess
# else:
#     errormess = '''Sorry, I cannot find %s.
#     Please check wether PPlib is in the topspin directory.
#     ''' %parfile
#     raise Exception(errormess)

# Add bits.sg for correct channel assignment
bits = os.path.join(top, 'exp/stan/nmr/lists/pp/user/bits.sg')
bits = bits.replace('/', os.sep)
if os.path.isfile(bits):
    print '%s already exists' % os.path.join(top, 'exp/stan/nmr/lists/pp/user/bits.sg')
else:
    shutil.copy(os.path.join(PPlib, 'bits.sg'),
                os.path.join(top, 'exp/stan/nmr/lists/pp/user'))
    print 'Added bits.sg to %s' % os.path.join(top, 'exp/stan/nmr/lists/pp/user')
