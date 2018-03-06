#! /usr/bin/env python

import os, sys, re, getopt, datetime

setup_path = '/opt/topspin3.2pl7/PPlib'
sys.path.append(os.path.join(setup_path, 'py' ))

import ppGlobals as pp
import ppUtil as ut
import ppSpect as spec
import fcalc

from javax.swing import JFrame, JFileChooser, JPanel
from java.awt import BorderLayout
from java.io import File

# frame = JFrame('test')
# chooseFile = JFileChooser()
# chooseFile.setCurrentDirectory(File(pp.iPulse_path))
# ret = chooseFile.showOpenDialog(frame)
# if ret == JFileChooser.APPROVE_OPTION:
#     file = chooseFile.getSelectedFile()
#     pp1 = file.getCanonicalPath()


class DigDown(JFrame):

    def __init__(self):
        super(DigDown, self).__init__()

        self.initUI()

    def initUI(self):

        self.panel = JPanel()
        self.panel.setLayout(BorderLayout())

        chooseFile = JFileChooser()
        chooseFile.setCurrentDirectory(File(pp.iPulse_path))
        chooseFile.setDialogTitle('Select Export Location')
        chooseFile.setFileSelectionMode(JFileChooser.DIRECTORIES_ONLY)

        ret = chooseFile.showOpenDialog(self.panel)

        if ret == JFileChooser.APPROVE_OPTION:
            if chooseFile.getSelectedFile().isDirectory():
                self.dir_path = str(chooseFile.getSelectedFile())

    def get_dir_path(self):
        return self.dir_path

    def get_dir_name(self):
        return self.dir_path.rsplit(os.sep, 1)[-1]


if __name__ == '__main__':
    test = DigDown()
    print test.get_dir_path()
    print test.get_dir_name()
