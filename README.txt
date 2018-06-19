NMRPulse Version 0.00.00

=======================


Description
-------------

This project contains a library of Bruker pulse programs and Python set up scripts for easy sharing of NMR experiments.
Bruker pulse programs are extended with a Python header which defines the relevant parameters for the experiment.
The corresponding parameters are set by the Python scripts and take the spectrometer type into account.

How to install
--------------------------

- After downloading this folder, move it to the Topspin directory of the local spectrometer.
- Run setup.py



How to use
--------------------------

In order to set up a new experiment execute the ppExpSetupGUI.py script from the Topspin command line. This will perform the following tasks:

	- Choose the experiment
	- Read standard parameter set based on experiment type (defines correct routing to spectrometer)
	- Load corresponding pulse program 
	- Relevant acquisition parameters are set
	- Waveform, gradient, CPD files and other relevant subcomponents are loaded to Topspin
	- Relevant processing parameters are set

The parameters are now loaded. Note that starting the experiment, shimming, tuning and P1 calibration are still required.


Dependencies
--------------------------
#####TO DO: List dependencies
Python 2.7
Jython 