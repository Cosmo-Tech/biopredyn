# - Find XSD
# This module finds an installed XSD.  It sets the following variables:
#  XSD_FOUND - set to true if XSD is found
#  XSD_EXECUTABLE - the path to the swig executable

SET(XSD_FOUND 0)

FIND_PROGRAM(XSD_EXECUTABLE xsd
  PATHS /usr/bin /usr/local/bin )

IF(XSD_EXECUTABLE)
  SET(XSD_FOUND 1)
  MESSAGE(STATUS "Found XSD: ${XSD_EXECUTABLE}")
ENDIF()

IF(NOT XSD_FOUND)
  MESSAGE(FATAL_ERROR "XSD was not found on the system. Please specify the location of XSD.")
ENDIF()
