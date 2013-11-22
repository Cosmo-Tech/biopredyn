BioPreDyn prototype installation

1. Ubuntu (11.10 or later)
1.1 Dependencies
1.1.1 CMake
sudo apt-get install cmake
sudo apt-get install cmake-curses-gui

1.1.2 Subversion
sudo apt-get install subversion

1.1.3 Python
sudo apt-get install python2.7

1.1.4 SWIG
sudo apt-get install swig2.0

1.1.5 libXML2
sudo apt-get install libxml2

1.1.6 Autoconf
sudo apt-get install autoconf

1.1.7 Automake
sudo apt-get install automake

1.1.8 Libtool
sudo apt-get install libtool

1.1.9 XSLT processor
sudo apt-get install xsltproc

1.1.10 Expat
sudo apt-get install libexpat1 libexpat1-dev

1.1.11 libbzip2
Download the latest package from http://www.bzip.org/, extract it. Go to the
newly created directory then type the following commands:
make
make install

1.1.12 easy_install
Download ez_setup.py from https://bitbucket.org/pypa/setuptools/downloads then
execute the following command in the folder containing the file:
sudo python ez_setup.py

1.1.13 matplotlib
sudo easy_install matplotlib

1.1.14 libSBML
Download the latest stable version at http://sbml.org/Software/libSBML, then
run the installer.

1.2 Package

mkdir build
cd build
cmake ..
make
make install
make test

2. Windows 7 (32 bits)
2.1 Dependencies
2.1.1 CMake
Download the latest stable version from
http://www.cmake.org/cmake/resources/software.html, then run the installer
and follow the instructions.

2.1.2 Microsoft Visual Studio 2010 Express
Download the C++ version from
http://www.visualstudio.com/en-us/downloads/download-visual-studio-vs#DownloadFamilies_4
Run the executable and follow the instructions.

2.1.3 Subversion
Download Apache Subversion from http://www.visualsvn.com/downloads/, run the
installer and follow the instructions.

2.1.4 Python 2.7
Download the Windows installer from http://www.python.org/download/, run it
and follow the instructions.

2.1.5 SWIG
The latest version of swigwin can be downloaded from
http://www.swig.org/download.html. Unzip it then add the folder containing
swig.exe to the Path environment variable.

sudo apt-get install autoconf
sudo apt-get install automake
sudo apt-get install libtool
sudo apt-get install xsltproc
sudo apt-get install libexpat1 libexpat1-dev

libbzip2: download the latest package from http://www.bzip.org/, extract it,
then do a make / make install

easy_install: download ez_setup.py from
https://bitbucket.org/pypa/setuptools/downloads then: sudo python ez_setup.py

sudo easy_install matplotlib

libsbml: download the latest stable version at
http://sbml.org/Software/libSBML, install it