PPlib Version 0.00.00

=======================


Description
-------------

This project contains a library of Bruker pulse programs and Python set up scripts for easy sharing of NMR experiments.
Bruker pulse programs are extended with a Python header which defines the relevant parameters for the experiment.
The corresponding parameters are set by the Python scripts and take the spectrometer type into account.

How to install
--------------------------

####TO DO: Good question…
-Install this folder in the topspin directory
- Run setup.py



How to use
--------------------------

In order to set up a new experiment a Python script is executed which performs the following tasks:

	- Choose the experiment
	- Read standard parameter set based on experiment type (defines correct routing to spectrometer)
	- Load corresponding pulse program 
	- Relevant acquisition parameters are set
	- #####TO DO?: Relevant processing parameters are set


Dependencies
--------------------------
#####TO DO: List dependencies
Python 2.7