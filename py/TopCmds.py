"""\
 *******************************************************************
 *
 * $Source: /pr/CvsTree/pr/gen/java/src/de/bruker/nmr/py/pycmd/TopCmds.py,v $
 *
 * Copyright (c) 1999 - 2013
 * Bruker BioSpin GmbH
 * D-76287 Rheinstetten, Germany
 *
 * All Rights Reserved
 *
 *
 * $State: Exp $
 * $Id: TopCmds.py,v 1.106.4.1.2.6 2013/08/29 12:07:12 es Exp $
 *
 *******************************************************************
                      
                  !!!! I M P O R T A N T   !!!!
         
         When you add a function to this file, also add its documentation
         to the function table in the file
             de/bruker/nmr/doc/english/src/python.odt
        
"""
from java.lang import *

import de.bruker.nmr as nmr
import de.bruker.nmr.mfw.base as mfw
import de.bruker.nmr.mfw.root as root
import de.bruker.nmr.mfw.dialogs as dialogs
import de.bruker.nmr.prsc.cpr as cpr
import de.bruker.nmr.prsc.toplib as top
import de.bruker.data.Constants as dataconst
import de.bruker.nmr.prsc.util as putil
import de.bruker.nmr.pr.browse as browse
import de.bruker.nmr.pr as pr
import de.bruker.nmr.prsc as prsc
import de.bruker.nmr.sc as sc
import sys
import time

"""\
	This Python module defines functions that allow one to simply
	execute TOPSPIN command from a Python program.
"""
WAIT_TILL_DONE = 1;
NO_WAIT_TILL_DONE = 0;


# TopSpin commands
#/******************/
# execute an arbitrary TOPSPIN command
def XCMD(cmd, wait = WAIT_TILL_DONE, arg = None):
	return top.Cmd.exec(cmd, wait, arg)

# execute an arbitrary CPR command
def XCPR(cmd, wait = WAIT_TILL_DONE):
	return top.Cmd.exec(cmd, wait, "$$$CPR")

# execute a py script in an own CmdThread
def EXEC_PYSCRIPT(pyscript, arg = None):
	return mfw.PythonStarter().execPyscript(pyscript, arg)

# execute a py file in an own CmdThread
def EXEC_PYFILE(pyfile, arg = None):
	return mfw.PythonStarter().execPyFile(pyfile, arg)

#
# OS utilities
#
def SLEEP(secs):
	time.sleep(secs)

# get the host name
def GETHOSTNAME():
	return nmr.jutil.misc.UtilOS.getHostName()

# Parameter commands
#/******************/
def GETPAR2(name):
    return top.Cmd.getPar2(name)

def GETPAR(name, axis = 0):
	return top.Cmd.getPar(name, axis, 0)

def GETPARSTAT(name, axis = 0):
	return top.Cmd.getPar(name, axis, 1)

def PUTPAR(name, value, dataspecs = None):
	return top.Cmd.putPar(name, value, dataspecs)

def GETPROCDIM():
	return top.Cmd.getDim(0)

def GETACQUDIM():
	return top.Cmd.getDim(1)


def GETPARS(names, axis=0, status = 0):
	'''Get values for a TopSpin parameter list:
names - a vector of parameter names, e.g. SI, P 1,  etc.
axis - 1 2 3, .. (0 = acquisition dim.)
Returns the values as a string array
'''
	return top.Cmd.getPars(names, axis, status)


# Data set handling commands
#/**************************/

#   dataset = [name, expno, procno, dir] 
def NEWDATASET(dataset, aexpdir = None, aexp = "PROTON"):
	aname = dataset[0]
	aexpno = dataset[1]
	aprocno = dataset[2]
	adir = dataset[3]
	top.NMRDataFactory.creatData(adir, aname, aexpno, aprocno, aexpdir, aexp)

#   dataset = [name, expno, procno, dir] 
def RE(dataset = None, show = "y"):
	top.Cmd.re(dataset, show)

def RE_PATH(datapath = None, show = "y"):
	top.Cmd.repath(datapath, show)

def RSER(fidnum = None, expno = None, show = "y"):
	top.Cmd.rser(fidnum, expno, show)

def RSR(num = None, procno = None, show = "y"):
	top.Cmd.rsc(num, procno, show, "rsr")

def RSC(num = None, procno = None, show = "y"):
	top.Cmd.rsc(num, procno, show, "rsc")

def WR(dataset = None, confirm="y"):
	top.Cmd.wr(dataset, confirm)

def WR_PATH(datapath = None, confirm="y"):
	top.Cmd.wr(datapath, confirm)

def CURDATA(cmdthread = None):
	return top.Cmd.curdata(cmdthread)
	
# set curdat2 file for the currently active dataset	
def SET_CURDATA2(dir2, user2, name2, expno2, procno2):
	nmrdatapars = prsc.util.DataChecks.getNMRDataOfSelectedFramePrintMsg().getProperties()
	nmrdatapars.setProperty("CURDAT2", nmr.jutil.xwin.UtilXwin.mkXwinDataPath(dir2, user2, name2, expno2, procno2))	

# incs the expno of the specified data set or the curdat and reads the new data set
def RE_IEXPNO(dataset=None, show = "y"):
	if(dataset==None): dataset = CURDATA()
	if(dataset==None): EXIT("No dataset defined")
	expno = int(dataset[1])
	dataset[1] = str(expno+1)
	RE(dataset, show)
	
# incs the procno of the specified data set or the curdat and reads the new data set
def RE_IPROCNO(dataset=None, show = "y"):
	if(dataset==None): dataset = CURDATA()
	if(dataset==None): EXIT("No dataset defined")
	procno = int(dataset[2])
	dataset[2] = str(procno+1)
	RE(dataset, show)

# type = dataconst.PROCDATA_REAL(=None), dataconst.PROCDATA_IMAG, ....
def GETPROCDATA(fromppm, toppm, type = None):
	return top.Cmd.getProcData(fromppm, toppm, type)
	
def GETPROCDATA2D(from1, to1, from2, to2, type = None):
	return top.Cmd.getProcData2D(from1, to1, from2, to2, type)

def GET_DISPLAY_PROPS(xStart = None, xEnd = None, xUnit = None, xLegend=None,
			yLegend=None, dataTitle=None, drawMode="line", yscaleRef = None, yStart = None, yEnd = None):
		return [str(xStart), str(xEnd), xUnit, xLegend,
			yLegend, dataTitle, drawMode, yscaleRef, str(yStart), str(yEnd)]

def DISPLAY_DATALIST(ydataList, propList = None, winTitle = "",
		multipleView = 0):
	return top.GraphExtend.displayDataList(ydataList, None, propList, winTitle, multipleView)

def DISPLAY_DATALIST_XY(ydataList, xdataList, propList = None, winTitle = "", multipleView = 0):
	return top.GraphExtend.displayDataList(ydataList, xdataList, propList, winTitle, multipleView)

#type="Any"; "spectra"; "fids"; "1D+2D+3D";"1D+2D";"1D";"2D";"3D";
def FIND_DATA(dirlist, name="", expno="", procno="", user="", title="", pulprog="",	dim="", type=""):
	filelist = putil.XwinFileList.findDatasets([name, expno, procno, user],
		dirlist, title, pulprog, putil.XwinFileList.FindDataDim.toEnum(dim),
        putil.XwinFileList.FindDataType.toEnum(type), -1, -1, None)
	return filelist

def SAVE_ARRAY_AS_1R1I(reals, imags, dataspecs=None, offset=0.0, sw=0.0):
	if dataspecs is None:
		dataspecs=top.Cmd.curdata(None)
	return top.NMRDataFactory().saveAs1r1i(reals, imags, dataspecs, offset, sw)

def SAVE_ARRAY_AS_2RR(reals, imags,sizes, dataspecs = None, fromData = None, experiment = None):
	if dataspecs is None:
		dataspecs=top.Cmd.curdata(None)
	return top.NMRDataFactory().saveAs2rr2ii(reals, imags,sizes, dataspecs, fromData, experiment)
	

# Functions for internal frame (window) handling
#/**********************************************/
# create new internal window

def NEWWIN(width = -1, height = -1):
	return top.Win.newUserPanel("",width,height)
	
# Close the internal window containing a specified data set
# data set to be specified as a list [name, expno, procno, dir, user]
# if dataset = None close all windows
# Alternatively the frame id may be specified
def CLOSEWIN(dataset = None, winid = None):
	if winid != None:
		desktop = root.Globals.mainDataPanel.getDesktop()
		desktop.closeFrame(desktop.getInFrameWithId(winid))
	else:	
		top.Win.closewin(dataset)

# Arrange the internal windows in TOPSPIN
# mode = $m = mixed, $v = vertically, $h = horizontally
# anything else is a layout filename
def ARRANGE(mode = "$v"):
	top.Win.arrange(mode, 0)
	
def ARRANGE_WIN(winid, x, y, width, height):
	mfw.UtilDesktop().arrangeWin(winid, x, y, width, height)

# Position selected window according to layout file
def POSITION_WIN(file = None):
	top.Win.arrange(file, 1)

# Position window of specified type according to layout file
def POSITION_WINTYPE(frameType = "DATA_WINDOW", file = None):
	mfw.UtilDesktop.arrangeWinFromFile(frameType, file)

# select a TAB in the current data window
# For type must use DatasetPane.PROCPARS etc.
def SELECT_TAB(type):
	top.Win.selectTab(type)

def SELECT_CURDAT_WIN():
	top.Win.setCmdThreadCurdatWinSelected()

# Get the window which was active when this script was started
#
def SCRIPT_WINDOW():
	desktop = root.Globals.mainDataPanel.getDesktop()
	CT = Thread.currentThread()
	frameId = CT.getFrameId()
	return desktop.getInFrameWithId(frameId)
	
def GETWINID(userPanel = None):
	if userPanel == None:
		if SCRIPT_WINDOW() == None:
			return None
		else:
			userPanel = SCRIPT_WINDOW().getUserPanelData()
	if userPanel == None:
		return None
	else:
		return mfw.BDesktop.getInFrame(userPanel).getId()

# Get the currently active window.
# Returns an java de.bruker.nmr.mfw.base.InFrame object
#
def SELECTED_WINDOW():
	desktop = root.Globals.mainDataPanel.getDesktop()
	return desktop.getSelectedIntFrame()

# Get the currently active window and set the command threat dataset to this window.
# Global CMDTHREAD should be used as parameter for this function
#
def SET_DATASET(CMDTHREAD = None):
	inFrame = root.Globals.mainDataPanel.getDesktop().getSelectedIntFrame()
	if CMDTHREAD == None:
		#no argument specified => use currentThread instead
		CMDTHREAD = Thread.currentThread()
			
	CMDTHREAD.setDataObject(inFrame.getDataObject())
	CMDTHREAD.setFrameId(inFrame.getId())
	
def SET_SELECTED_WIN(winid):
	inFrame = root.Globals.mainDataPanel.getDesktop().getInFrameWithId(winid)
	ct = Thread.currentThread()
	ct.setDataObject(inFrame.getDataObject())
	ct.setFrameId(winid)

# Switch the next window to be active (selected)
#
def SELECT_NEXT_WINDOW():
	mfw.UtilDesktop.nextWin()

# Return an array of all internal windows in the creation order
# (java de.bruker.nmr.mfw.base.InFrame type)
#
def ALL_WINDOWS():
	desktop = root.Globals.mainDataPanel.getDesktop()
	return desktop.getAllInFrames()


# Dialogs
#/*******/
def INPUT_DIALOG(title=None, header=None, items=None, values=None, comments=None, types=None, buttons=None, mnemonics=None, columns = 30):
  dia = dialogs.MultiLineInputDia(title, header, items, values, types, comments, buttons, mnemonics, 0, columns, 1, None)
  return dia.getValues()

def DATASET_DIALOG(title=None, values=None):
  dia = putil.DatasetDia(title, values)
  return dia.getValues()

def FIND_DIALOG(options="get_selected"):
	return prsc.databrowsers.FindDataDia().findDialog(options)

def MSG(message = "", title=None, details=None):
	dia = mfw.BInfo() # BInfo has no details button, so details arg is not evaluated
	dia.setMessage(message)
	dia.setMsgSource(details)
	dia.setTitle(title)
	dia.setBlocking(1)
	dia.show()

def ERRMSG(message = "",title=None, details=None, modal=0):
	dia = mfw.BError()
	dia.setMessage(message)
	dia.setTitle(title)
	dia.setMsgSource(details)
	dia.setBlocking(modal)
	dia.show()

def CONFIRM(title=None, message=""):
	return root.Msg.confirm(title, message)

def SELECT(title=None, message="", buttons=["OK_M", "CANCEL_M"], mnemonics=None):
	return root.Msg.selectPy(title, message, buttons, mnemonics)

def VIEWTEXT(title="", header="", text="", modal=1):
	return nmr.mfw.edit.TextViewer(text, title, header, modal)


# Message printing
#/****************/
# Display a message in the status line of TOPSPIN
def SHOW_STATUS(message = ""):
	mfw.MainFrame.showStatus(message)


# Control commands
#/****************/
def EXIT(error = ""):
	sys.exit(error + "DONT_PRINT_CANCELLED_MESSAGE")

# Peak Picking commands
#/*********************/
# argument options: append = "append", dia = "y"
# append currently supported for 2D only
def PP(append = "", dialog = "nodia", wait = WAIT_TILL_DONE):
	return top.Cmd.exec("pp " + " " + dialog + " " + append, wait)

def MDCON(wait = WAIT_TILL_DONE):
	return top.Cmd.exec("mdcon", wait, "$$$CPR")

def PPP(wait = WAIT_TILL_DONE):
	return top.Cmd.exec("ppp", wait, "$$$CPR")

def GETPEAKSFILE():
	return top.Cmd.getPeaksFile();

def GETPEAKSARRAY():
	return top.Cmd.getPeaksArray();


#	Acquisition commands
#/********************/
def ASED(wait = WAIT_TILL_DONE):
	return top.Cmd.exec("ased", wait)
	
def ZG(wait = WAIT_TILL_DONE):
	return top.Cmd.exec("zg", wait)

def GO(wait = WAIT_TILL_DONE):
	return top.Cmd.exec("go", wait)

def GS(wait = WAIT_TILL_DONE):
	return top.Cmd.exec("gs", wait)

def WOBB(wait = WAIT_TILL_DONE):
	return top.Cmd.exec("wobb", wait)

def BSMSDISP(wait = NO_WAIT_TILL_DONE):
	return top.Cmd.exec("bsmsdisp", wait)

def LOCKDISP(wait = NO_WAIT_TILL_DONE):
	return top.Cmd.exec("lockdisp", wait)

def EDTE(wait = NO_WAIT_TILL_DONE):
	return top.Cmd.exec("edte", wait)


#	Pulse Program utilities
#/***********************/

def DEF_PULSPROG(ppText):
	return prsc.dbxml.PPUtils(ppText)
	
def SAVE_SHAPE(name, type, amplitude, phase):
	return sc.shapetool.UserDefShape(name, type, amplitude, phase)
	
def SAVE_GRADIENT(name, amplitude):
	return sc.shapetool.UserDefShape(name, amplitude)
	
# destination = [name, expno, procno, dir]	
def SAVE_SHAPE_AS_DATASET(amplitude, phase, destination, offset, sw):	
	return prsc.toplib.NMRDataFactory.saveAsDataset(amplitude, phase, destination, offset,
							 sw, None, None)	

def GET_PULSPROG_TEXT(ppName):
	return prsc.dbxml.DBHandlerPP().getPulsProgText(ppName)


#	PROCESSING COMMANDS
#/*******************/
def ABS(wait = WAIT_TILL_DONE):
	return top.Cmd.exec("abs", wait)

def ABSD(wait = WAIT_TILL_DONE):
	return top.Cmd.exec("absd", wait)

def ABSF(absf1=float(sys.maxint), absf2=float(sys.maxint), wait = WAIT_TILL_DONE):
	if absf1 < sys.maxint:
		top.Cmd.putPar("ABSF1", str(absf1))
	if absf2 < sys.maxint:
		top.Cmd.putPar("ABSF2", str(absf2))
	return top.Cmd.exec("absf", wait)

def APK(wait = WAIT_TILL_DONE):
	return top.Cmd.exec("apk", wait)

def APK0(wait = WAIT_TILL_DONE):
	return top.Cmd.exec("apk0", wait)

def APK1(wait = WAIT_TILL_DONE):
	return top.Cmd.exec("apk1", wait)

def APKF(wait = WAIT_TILL_DONE):
	return top.Cmd.exec("apkf", wait)

def APKS(wait = WAIT_TILL_DONE):
	return top.Cmd.exec("apks", wait)

def BC(wait = WAIT_TILL_DONE):
	return top.Cmd.exec("bc same", wait)

def BCM(wait = WAIT_TILL_DONE):
	return top.Cmd.exec("bcm", wait)

def EF(wait = WAIT_TILL_DONE):
	return top.Cmd.exec("ef same", wait)

def EFP(wait = WAIT_TILL_DONE):
	return top.Cmd.exec("efp same", wait)

def EM(lb = float(sys.maxint), wait = WAIT_TILL_DONE):
	if lb < sys.maxint:
		top.Cmd.putPar("LB", str(lb))
	return top.Cmd.exec("em same", wait)

def FMC(wait = WAIT_TILL_DONE):
	return top.Cmd.exec("fmc same", wait)

def FT(si = -1, wait = WAIT_TILL_DONE):
	if si > 0:
		top.Cmd.putPar("SI", str(si))
	return top.Cmd.exec("ft same", wait)

def FP(wait = WAIT_TILL_DONE):
	return top.Cmd.exec("fp same", wait)

def GF(wait = WAIT_TILL_DONE):
	return top.Cmd.exec("gf same", wait)

def GFP(wait = WAIT_TILL_DONE):
	return top.Cmd.exec("gfp same", wait)

def GM(lb = float(sys.maxint), gb = float(sys.maxint), wait = WAIT_TILL_DONE):
	if lb < sys.maxint:
		top.Cmd.putPar("LB", str(lb))
	if gb < sys.maxint:
		top.Cmd.putPar("GB", str(gb))
	return top.Cmd.exec("gm same", wait)

def HT(wait = WAIT_TILL_DONE):
	return top.Cmd.exec("ht", wait)

def IFT(wait = WAIT_TILL_DONE):
	return top.Cmd.exec("ift", wait)

def MC(wait = WAIT_TILL_DONE):
	return top.Cmd.exec("mc", wait)

def PK(phc0 = float(sys.maxint), phc1 = float(sys.maxint), wait = WAIT_TILL_DONE):
	if phc0 < sys.maxint:
		top.Cmd.putPar("PHC0", str(phc0))
	if phc1 < sys.maxint:
		top.Cmd.putPar("PHC1", str(phc1))
	return top.Cmd.exec("pk", wait)

def PS(wait = WAIT_TILL_DONE):
	return top.Cmd.exec("ps", wait)

def QSIN(wait = WAIT_TILL_DONE):
	return top.Cmd.exec("qsin same", wait)

def SAB(wait = WAIT_TILL_DONE):
	return top.Cmd.exec("sab", wait)

def SINM(wait = WAIT_TILL_DONE):
	return top.Cmd.exec("sinm same", wait)

def SREF(wait = WAIT_TILL_DONE):
	return top.Cmd.exec("sref", wait)

def TM(wait = WAIT_TILL_DONE):
	return top.Cmd.exec("tm same", wait)

def TRF(wait = WAIT_TILL_DONE):
	return top.Cmd.exec("trf same", wait)

def TRFP(wait = WAIT_TILL_DONE):
	return top.Cmd.exec("trfp", wait)

def UWM(wait = WAIT_TILL_DONE):
	return top.Cmd.exec("uwm same", wait)

def GENFID(num, wait = WAIT_TILL_DONE):
	return top.Cmd.exec("genfid " + str(num) + "y n", wait)

def CONVDTA(num, wait = WAIT_TILL_DONE):
	return top.Cmd.exec("convdta " + str(num) + "y n", wait)

"""
# Algebra commands
#/****************/
def ADD	SETCURDATA AUERR=CPR_exec("add",WAIT_TERM);
def ADDFID	SETCURDATA AUERR=CPR_exec("addfid y",WAIT_TERM);
def ADDC	SETCURDATA AUERR=CPR_exec("addc",WAIT_TERM);
def ADSU	SETCURDATA AUERR=CPR_exec("adsu",WAIT_TERM);
def AND	SETCURDATA AUERR=CPR_exec("and",WAIT_TERM);
def AT	SETCURDATA AUERR=CPR_exec("at",WAIT_TERM);
def CMPL	SETCURDATA AUERR=CPR_exec("cmpl",WAIT_TERM);
def DIV	SETCURDATA AUERR=CPR_exec("div",WAIT_TERM);
def DT	SETCURDATA AUERR=CPR_exec("dt",WAIT_TERM);
def FILT	SETCURDATA AUERR=CPR_exec("filt",WAIT_TERM);
def LS	SETCURDATA AUERR=CPR_exec("ls",WAIT_TERM);
def MUL	SETCURDATA AUERR=CPR_exec("mul",WAIT_TERM);
def MULC	SETCURDATA AUERR=CPR_exec("mulc",WAIT_TERM);
def NM	SETCURDATA AUERR=CPR_exec("nm",WAIT_TERM);
def RS	SETCURDATA AUERR=CPR_exec("rs",WAIT_TERM);
def RV	SETCURDATA AUERR=CPR_exec("rv",WAIT_TERM);
def ZF	SETCURDATA AUERR=CPR_exec("zf",WAIT_TERM);
def ZP	SETCURDATA AUERR=CPR_exec("zp",WAIT_TERM);
"""

# 2D processing commands
#/**********************/
def ABS1(wait = WAIT_TILL_DONE):
	return top.Cmd.exec("abs1", wait)
def ABS2(wait = WAIT_TILL_DONE):
	return top.Cmd.exec("abs2", wait)
def ABSD1(wait = WAIT_TILL_DONE):
	return top.Cmd.exec("absd1", wait)
def ABSD2(wait = WAIT_TILL_DONE):
	return top.Cmd.exec("absd2", wait)
def ABSOT1(wait = WAIT_TILL_DONE):
	return top.Cmd.exec("absot1", wait)
def ABSOT2(wait = WAIT_TILL_DONE):
	return top.Cmd.exec("absot2", wait)
def ABST1(wait = WAIT_TILL_DONE):
	return top.Cmd.exec("abst1", wait)
def ABST2(wait = WAIT_TILL_DONE):
	return top.Cmd.exec("abst2", wait)
def ADD2D(wait = WAIT_TILL_DONE):
	return top.Cmd.exec("add2d", wait)
def ADDSER(wait = WAIT_TILL_DONE):
	return top.Cmd.exec("addser", wait)
def BCM1(wait = WAIT_TILL_DONE):
	return top.Cmd.exec("bcm1", wait)
def BCM2(wait = WAIT_TILL_DONE):
	return top.Cmd.exec("bcm2", wait)
def INVSF(wait = WAIT_TILL_DONE):
	return top.Cmd.exec("invsf", wait)
def LEVCALC(wait = WAIT_TILL_DONE):
	return top.Cmd.exec("levcalc", wait)
def PTILT(wait = WAIT_TILL_DONE):
	return top.Cmd.exec("ptilt", wait)
def PTILT1(wait = WAIT_TILL_DONE):
	return top.Cmd.exec("ptilt1", wait)
def REV1(wait = WAIT_TILL_DONE):
	return top.Cmd.exec("rev1", wait)
def REV2(wait = WAIT_TILL_DONE):
	return top.Cmd.exec("rev2", wait)
def SUB1(wait = WAIT_TILL_DONE):
	return top.Cmd.exec("sub1", wait)
def SUB2(wait = WAIT_TILL_DONE):
	return top.Cmd.exec("sub2", wait)
def SUB1D1(wait = WAIT_TILL_DONE):
	return top.Cmd.exec("sub1d1", wait)
def SUB1D2(wait = WAIT_TILL_DONE):
	return top.Cmd.exec("sub1d2", wait)
def SYM(wait = WAIT_TILL_DONE):
	return top.Cmd.exec("sym", wait)
def SYMA(wait = WAIT_TILL_DONE):
	return top.Cmd.exec("syma", wait)
def SYMJ(wait = WAIT_TILL_DONE):
	return top.Cmd.exec("symj", wait)
def TILT(wait = WAIT_TILL_DONE):
	return top.Cmd.exec("tilt", wait)
def XF1(wait = WAIT_TILL_DONE):
	return top.Cmd.exec("xf1", wait)
def XF1P(wait = WAIT_TILL_DONE):
	return top.Cmd.exec("xf1p", wait)
def XF2(wait = WAIT_TILL_DONE):
	return top.Cmd.exec("xf2 same", wait)
def XF2P(wait = WAIT_TILL_DONE):
	return top.Cmd.exec("xf2p", wait)
def XFB(wait = WAIT_TILL_DONE):
	return top.Cmd.exec("xfb same", wait)
def XFBP(wait = WAIT_TILL_DONE):
	return top.Cmd.exec("xfbp", wait)
def XF1M(wait = WAIT_TILL_DONE):
	return top.Cmd.exec("xf1m", wait)
def XF2M(wait = WAIT_TILL_DONE):
	return top.Cmd.exec("xf2m", wait)
def XFBM(wait = WAIT_TILL_DONE):
	return top.Cmd.exec("xfbm", wait)
def XF1PS(wait = WAIT_TILL_DONE):
	return top.Cmd.exec("xf1ps", wait)
def XF2PS(wait = WAIT_TILL_DONE):
	return top.Cmd.exec("xf2ps", wait)
def XFBPS(wait = WAIT_TILL_DONE):
	return top.Cmd.exec("xfbps", wait)
def XHT1(wait = WAIT_TILL_DONE):
	return top.Cmd.exec("xht1", wait)
def XHT2(wait = WAIT_TILL_DONE):
	return top.Cmd.exec("xht2", wait)
def XIF1(wait = WAIT_TILL_DONE):
	return top.Cmd.exec("xif1", wait)
def XIF2(wait = WAIT_TILL_DONE):
	return top.Cmd.exec("xif2", wait)
def XTRF(wait = WAIT_TILL_DONE):
	return top.Cmd.exec("xtrf same", wait)
def XTRF2(wait = WAIT_TILL_DONE):
	return top.Cmd.exec("xtrf2 same", wait)
def XTRFP(wait = WAIT_TILL_DONE):
	return top.Cmd.exec("xtrfp", wait)
def XTRFP1(wait = WAIT_TILL_DONE):
	return top.Cmd.exec("xtrfp1", wait)
def XTRFP2(wait = WAIT_TILL_DONE):
	return top.Cmd.exec("xtrfp2", wait)
def ZERT1(wait = WAIT_TILL_DONE):
	return top.Cmd.exec("zert1", wait)
def ZERT2(wait = WAIT_TILL_DONE):
	return top.Cmd.exec("zert2", wait)
def PROJ(wait = WAIT_TILL_DONE):
	return top.Cmd.exec("proj", wait)
def GENSER(num, wait = WAIT_TILL_DONE):
	return top.Cmd.exec("genser " + str(num) + "y n", wait)

PROCDATA_IMAG = "PROCDATA_IMAG"

