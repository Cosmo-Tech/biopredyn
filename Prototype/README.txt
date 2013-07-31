====================== BioPreDyn software suite prototype ======================

This code is the deliverable 7.2 of the BioPreDyn project ("Prototype Software
for Testing: User-friendly version of prototype software for testing in a
setting for industrial applications").

For more information about the development tasks related to the BioPreDyn
project (and the content of the deliverable 7.2), please visit the developer's
wiki: https://thecosmocompany.com/biopredyn-trac/

For more information about the BioPreDyn project itself, please refer to the
official project website: http://www.biopredyn.eu/

1. Installation

1.1. Dependencies

* CMake (http://www.cmake.org/): software build system.
* git (http://git-scm.com/): version control system; required for cloning the
libSEDML repository on GitHub.
* Python (version 2.7 or more - http://www.python.org/)
* libSBML (http://sbml.org/Software/libSBML): library for SBML file
manipulation; do not forget to build the library with Python bindings enabled.
* libSEDML (https://github.com/fbergmann/libSEDML): library for SED-ML file
manipulation; clone the https://github.com/fbergmann/libSEDML.git repository
with git and build the library with CMake, as described in the README.md file.
* COBRApy (http://sourceforge.net/projects/opencobra/files/python/cobra/0.2.1/):
library of tools for systems biology model analysis, originally a Matlab
toolbox; a Python version is now available.
* COPASI (http://www.copasi.org) Python bindings: library for the simulation and
analysis of biochemical networks.

1.2. Known problems

* libSEDML installation (Ubuntu 11.10): Python files are not completely
installed after running the installation process. A way to complete the
installation consists in manually putting the required files in
${INSTALL_DIR}/lib/python*/dist-packages and respecting the following folder
hierarchy:
${INSTALL_DIR}/lib/python*/dist-packages/libsedml.pth
${INSTALL_DIR}/lib/python*/dist-packages/libsedml/_libsedml.so
${INSTALL_DIR}/lib/python*/dist-packages/libsedml/libsedml.py
${INSTALL_DIR}/lib/python*/dist-packages/libsedml.pyc

* COPASI python bindings installation (Ubuntu 11.10): no setup file can be found
in the package, it therefore cannot be installed as a system library. The same
solution than the one described for libsedml can be used (with COPASI files
instead of libsedml files of course); alternatively, Eclipse users can simply
link the copasi*_python*_linux_x86 folder as an external library (in the project
properties).

2. User guide

2.1 Usage

python main.py /path/to/input/file [options]

Options can be:
--help: Display this help message.
--cobra: Open the input file using the cobrapy library.
--copasi: Open the input file using the Copasi library.
--sbml: Open the input file as an SBML model; SBML compliance will be checked.