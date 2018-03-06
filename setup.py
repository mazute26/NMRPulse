#! /usr/bin/env python
"""This macro is used to setup the PPlib project. It should be located in the
topspin directory.
"""

import os
import sys
import re

fpath = os.path.realpath(__file__)
PPlib = fpath.rsplit(os.sep, 1)[0]
version = '3.2pl7'
top = os.path.join(fpath.rsplit(os.sep, 2)[0], 'topspin%s' %version)
topo = os.path.join(fpath.rsplit(os.sep, 2)[0], 'topspin')

print 'PPlib: ', PPlib
print 'Top: ', top

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
    rex = r'%s *= *(?P<path>.+)' %dirname
    for line in lines:
        match = re.search(rex, line)
        if match:
            newline.append(line.replace(match.group('path'), '\'%s\'' %path))
        else:
            newline.append(line)
    f.close()
    fh=open(pyfile,'w')
    fh.writelines(newline)
    fh.close()
    return None

set_path(os.path.join(PPlib, 'py%sppGlobals.py' %os.sep), 'topspin_home', top)
set_path(os.path.join(PPlib, 'py%sppGlobals.py' %os.sep), 'setup_path', PPlib)
for files in os.listdir(os.path.join(PPlib, 'py')):
    if files.endswith('.py'):
        set_path(os.path.join(PPlib, 'py%s%s' %(os.sep, files)),'setup_path', PPlib)

#
# #Change Python path in parfile
# parfile = os.path.join(PPlib, '../classes/prop/parfile-dirs.prop')
# parfile = os.path.abspath(parfile)
# parfile = parfile.replace('/', os.sep)
#
# lines2 = []
# if os.path.isfile(parfile):
#     fh = open(parfile)
#     lines = fh.readlines()
#     for line in lines:
#         if 'PY_DIRS' in line:
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