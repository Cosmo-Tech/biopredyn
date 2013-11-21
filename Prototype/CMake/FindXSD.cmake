# - Find XSD
# This module finds an installed XSD.  It sets the following variables:
#  XSD_FOUND - set to true if XSD is found
#  XSD_EXECUTABLE - the path to the XSD executable
#  XSD_INCLUDE_DIR - XSD include directory

SET(XSD_FOUND 0)

FIND_PROGRAM(XSD_EXECUTABLE xsd2cpp
  PATHS /usr/bin /usr/local/bin )

find_path(XSD_INCLUDE_DIR
  NAMES XPlus/AutoPtr.h
  PATHS /usr/include
        /usr/local/include
        /opt/local/include
  )

IF(XSD_EXECUTABLE AND XSD_INCLUDE_DIR)
  SET(XSD_FOUND 1)
  MESSAGE(STATUS "Found XSD: ${XSD_EXECUTABLE}")
ENDIF()

IF(NOT XSD_FOUND)
  MESSAGE(FATAL_ERROR "XSD was not found on the system. Please specify the location of XSD.")
ENDIF()
