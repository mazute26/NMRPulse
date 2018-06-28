# NMRPulse

NMRPulse is an open platform that encourages the global exchange of NMR pulse sequences.
The framework contains a [library of NMR pulse programs](https://nmrpulse.biozentrum.unibas.ch) in which users and laboratories can find and download various experiments and are encouraged to share and upload their custom experiments.
Further, a set of Python scripts was developed to facilitate the setup of individual experiments on Bruker spectrometers.

## Getting Started

These instructions describe the functionality of the Python scripts which take care of installation, set up and creation NMRPulse experiments.

### Prerequisites

NMRPulse was development to facilitate the setup on Bruker spectrometers. Therefore the Topspin software as well as Python and Jython are required.

- Topspin
- Python
- Jython

### Installing

After downloading this folder, unzip the content and move it to the Topspin directory of the spectrometer disk.

Say what the step will be

```
$ cd /Downloads
$ unzip NMRPulse.zip
$ mv NMRPulse /opt/topspin3.2pl7/
```

Change to the NMRPulse directory and run the installation

```
$ python setup.py
```

It will ask you to enter the Topspin path. Enter it

```
/opt/topspin3.2pl7
```

## Further documentation

For more information and detailed instruction please see the Howto.pdf file or the [Getting started page](https://nmrpulse.biozentrum.unibas.ch/gettingstarted/) of the website.


## Release History

* 0.0.0
    * Development phase


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
