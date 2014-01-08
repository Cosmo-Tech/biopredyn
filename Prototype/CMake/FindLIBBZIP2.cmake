# - Find LIBBZIP2
# This module finds an installed libbzip2.  It sets the following variables:
#  LIBBZIP2_FOUND - set to true if libbzip2 is found
#  LIBBZIP2_LIBRARY - the path to the libbzip2 library

SET(LIBBZIP2_FOUND 0)

find_library(LIBBZIP2_LIBRARY 
  NAMES libbz2.so libbz2
  PATHS /lib/x86_64-linux-gnu/
        /usr/lib/x86_64-linux-gnu/
        /usr/lib/i386-linux-gnu/
        /usr/lib/
        /usr/lib64/
        /usr/local/lib/ )

IF(LIBBZIP2_LIBRARY)
  SET(LIBBZIP2_FOUND 1)
  MESSAGE(STATUS "Found LIBBZIP2: ${LIBBZIP2_LIBRARY}")
ENDIF()

IF(NOT LIBBZIP2_FOUND)
  MESSAGE(FATAL_ERROR "LIBBZIP2 was not found on the system. Please specify the location of LIBBZIP2.")
ENDIF()
