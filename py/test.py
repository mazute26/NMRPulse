#! /usr/bin/env python

import os, sys, re

import ppGlobals as pp

print 'add dir before: %s' % pp.addfiles_path


rex = r'iPulse/(?P<expname>\w+)/\d+'
rex2 = r'iPulse/(?P<expname>\w*)'

match = re.search(rex, pp.addfiles_path)
if match:
    print match.group('expname')

expname = 'askjfaja;d'

pp.addfiles_path = pp.addfiles_path.replace(match.group('expname'), expname)

print 'New add dir: %s' %pp.addfiles_path
