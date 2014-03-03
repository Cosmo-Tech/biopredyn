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

Windows: install easy_install too.

Windows: easy_install bioservices

Windows: lxml
  download latest package at https://pypi.python.org/pypi/lxml/
  (lxml-X.Y.Z.win32-py2.7.exe) and install it

2.1.6 PySide

2.1.6.1 Qt
  download the Qt4.8 library corresponding to your operating system on
  http://qt-project.org/downloads and install it.

2.1.6.2 PySide
  download the latest package (PySide-X.Y.Z.win32-py2.7.exe) at
  http://qt-project.org/wiki/PySide_Binaries_Windows and install it.

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

/!\ : warning when using libiconv from the CoSMo externals.
          Linking problem
          related to libiconv when building the library with
          cosmo-externals (for libxml); the file encoding.h must be
          modified in order to include <libiconv/iconv.h>
          instead of <iconv.h>. FRI: CMakeLists.txt should be modified
          in order to link the correct folder.