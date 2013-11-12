/**
* Begin svn Header
* $Rev: 26 $:	Revision of last commit
* $Author: josephodada@gmail.com $:	Author of last commit
* $Date: 2013-04-24 18:06:40 +0200 (Wed, 24 Apr 2013) $:	Date of last commit
* $HeadURL: http://numl.googlecode.com/svn/trunk/libnuml/examples/c++/readNUML.cpp $
* $Id: readNUML.cpp 26 2013-04-24 16:06:40Z josephodada@gmail.com $
* End svn Header
* ****************************************************************************
* This file is part of libNUML.  Please visit http://code.google.com/p/numl/for more
* information about NUML, and the latest version of libNUML.
* Copyright (c) 2013 The University of Manchester.
*
* This library is free software; you can redistribute it and/or modify it
* under the terms of the GNU Lesser General Public License as published
* by the Free Software Foundation.  A copy of the license agreement is
* provided in the file named "LICENSE.txt" included with this software
* distribution and also available online as http://www.gnu.org/licenses/lgpl.html
*
* Contributors:
* Joseph O. Dada, The University of Manchester - initial API and implementation
* ****************************************************************************
**/

#include <iostream>

#include <numl/NUMLTypes.h>
#include "util.h"


using namespace std;
LIBNUML_CPP_NAMESPACE_USE

int
main (int argc, char* argv[])
{
  if (argc != 2)
  {
    cout << endl << "Usage: readNUML filename" << endl << endl;
    return 1;
  }

  const char* filename   = argv[1];
  NUMLDocument* document;
  NUMLReader reader;
  unsigned long long start, stop;

  start    = getCurrentMillis();
  document = reader.readNUML(filename);
  stop     = getCurrentMillis();

  unsigned int errors = document->getNumErrors();

  cout << endl;
  cout << "            filename: " << filename              << endl;
  cout << "           file size: " << getFileSize(filename) << endl;
  cout << "      read time (ms): " << stop - start          << endl;
  cout << " validation error(s): " << errors << endl;
  cout << endl;

  document->printErrors(cerr);

  delete document;
  return errors;
}
