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

2.1.4 SWIG
The latest version of swigwin can be downloaded from
http://www.swig.org/download.html. Unzip it then add the folder containing
swig.exe to the Path environment variable.

2.1.5 Python
Download the Windows installer from http://www.python.org/download/, run it
and follow the instructions.

2.1.5.1 Python dependencies
2.1.5.1.1 easy_install
easy_install: download ez_setup.py from
https://bitbucket.org/pypa/setuptools/downloads then:
- execute ez_setup.py with Python
- add <path/to/python27>/Scripts to the Path

2.1.5.1.2 Numpy
Download it at http://sourceforge.net/projects/numpy/files/NumPy/1.8.1/numpy-1.8.1-win32-superpack-python2.7.exe/download
- install it.

2.1.5.1.3 Matplotlib
Download the installer for the last version (matplotlib-X.Y.Z.win32-py2.7.exe)
on https://github.com/matplotlib/matplotlib/downloads/; install it.

2.1.5.1.4 Other
easy_install easydev
easy_install bioservices
easy_install lxml
easy_install PySide

2.1.6 bzip2
Download the latest bzip2-X.Y.Z-setup.exe from http://sourceforge.net/projects/gnuwin32/files/bzip2/
and install it.

2.1.7 libXML2
Download the latest version (libxml2-X.Y.Z.win32.zip) at
http://xmlsoft.org/sources/win32/ and extract it. Add <path/to/libxml2>/include
to the environment path.

/!\ : warning when using libiconv from the CoSMo externals.
          Linking problem
          related to libiconv when building the library with
          cosmo-externals (for libxml); the file encoding.h must be
          modified in order to include <libiconv/iconv.h>
          instead of <iconv.h>. FRI: CMakeLists.txt should be modified
          in order to link the correct folder.