#! /usr/bin/env python
"""
Script to try stuff.
"""
import os, sys, re, getopt, datetime

setup_path = '/Users/mazute26/Documents/PP_SETUP/NMRPulse'
sys.path.append(os.path.join(setup_path, 'py' ))

import ppGlobals as pp
import ppUtil as ut
import ppSpect as spec
import fcalc
try:
    from javax.swing import JFrame, JFileChooser, JPanel
    from java.awt import BorderLayout
    from java.io import File
except:
    pass
try:
    import TopCmds as TC
except:
    pass

# frame = JFrame('test')
# chooseFile = JFileChooser()
# chooseFile.setCurrentDirectory(File(pp.iPulse_path))
# ret = chooseFile.showOpenDialog(frame)
# if ret == JFileChooser.APPROVE_OPTION:
#     file = chooseFile.getSelectedFile()
#     pp1 = file.getCanonicalPath()


# class DigDown(JFrame):
#
#     def __init__(self):
#         super(DigDown, self).__init__()
#
#         self.initUI()
#
#     def initUI(self):
#
#         self.panel = JPanel()
#         self.panel.setLayout(BorderLayout())
#
#         chooseFile = JFileChooser()
#         chooseFile.setCurrentDirectory(File(pp.iPulse_path))
#         chooseFile.setDialogTitle('Select Export Location')
#         chooseFile.setFileSelectionMode(JFileChooser.DIRECTORIES_ONLY)
#
#         ret = chooseFile.showOpenDialog(self.panel)
#
#         if ret == JFileChooser.APPROVE_OPTION:
#             if chooseFile.getSelectedFile().isDirectory():
#                 self.dir_path = str(chooseFile.getSelectedFile())
#
#     def get_dir_path(self):
#         return self.dir_path
#
#     def get_dir_name(self):
#         return self.dir_path.rsplit(os.sep, 1)[-1]

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

if __name__ == '__main__':
    pass
