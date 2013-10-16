# Install script for directory: /home/bertrand/Soft/libsbmlsim-1.1.0/src

# Set the install prefix
IF(NOT DEFINED CMAKE_INSTALL_PREFIX)
  SET(CMAKE_INSTALL_PREFIX "/usr/local")
ENDIF(NOT DEFINED CMAKE_INSTALL_PREFIX)
STRING(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
IF(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  IF(BUILD_TYPE)
    STRING(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  ELSE(BUILD_TYPE)
    SET(CMAKE_INSTALL_CONFIG_NAME "Release")
  ENDIF(BUILD_TYPE)
  MESSAGE(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
ENDIF(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)

# Set the component getting installed.
IF(NOT CMAKE_INSTALL_COMPONENT)
  IF(COMPONENT)
    MESSAGE(STATUS "Install component: \"${COMPONENT}\"")
    SET(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  ELSE(COMPONENT)
    SET(CMAKE_INSTALL_COMPONENT)
  ENDIF(COMPONENT)
ENDIF(NOT CMAKE_INSTALL_COMPONENT)

# Install shared libraries without execute permission?
IF(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  SET(CMAKE_INSTALL_SO_NO_EXE "1")
ENDIF(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)

IF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  IF(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/simulateSBML" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/simulateSBML")
    FILE(RPATH_CHECK
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/simulateSBML"
         RPATH "")
  ENDIF()
  FILE(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/bin" TYPE EXECUTABLE FILES "/home/bertrand/Soft/libsbmlsim-1.1.0/build/src/simulateSBML")
  IF(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/simulateSBML" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/simulateSBML")
    FILE(RPATH_REMOVE
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/simulateSBML")
    IF(CMAKE_INSTALL_DO_STRIP)
      EXECUTE_PROCESS(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/simulateSBML")
    ENDIF(CMAKE_INSTALL_DO_STRIP)
  ENDIF()
ENDIF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")

IF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  FILE(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE STATIC_LIBRARY FILES "/home/bertrand/Soft/libsbmlsim-1.1.0/build/src/libsbmlsim-static.a")
ENDIF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")

IF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  IF(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libsbmlsim.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libsbmlsim.so")
    FILE(RPATH_CHECK
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libsbmlsim.so"
         RPATH "")
  ENDIF()
  FILE(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE SHARED_LIBRARY FILES "/home/bertrand/Soft/libsbmlsim-1.1.0/build/src/libsbmlsim.so")
  IF(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libsbmlsim.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libsbmlsim.so")
    FILE(RPATH_REMOVE
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libsbmlsim.so")
    IF(CMAKE_INSTALL_DO_STRIP)
      EXECUTE_PROCESS(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libsbmlsim.so")
    ENDIF(CMAKE_INSTALL_DO_STRIP)
  ENDIF()
ENDIF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")

IF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  FILE(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/libsbmlsim" TYPE FILE FILES
    "/home/bertrand/Soft/libsbmlsim-1.1.0/src/libsbmlsim/myReaction.h"
    "/home/bertrand/Soft/libsbmlsim-1.1.0/src/libsbmlsim/errorcodes.h"
    "/home/bertrand/Soft/libsbmlsim-1.1.0/src/libsbmlsim/myResult.h"
    "/home/bertrand/Soft/libsbmlsim-1.1.0/src/libsbmlsim/mySpecies.h"
    "/home/bertrand/Soft/libsbmlsim-1.1.0/src/libsbmlsim/myEvent.h"
    "/home/bertrand/Soft/libsbmlsim-1.1.0/src/libsbmlsim/dSFMT-params521.h"
    "/home/bertrand/Soft/libsbmlsim-1.1.0/src/libsbmlsim/methods.h"
    "/home/bertrand/Soft/libsbmlsim-1.1.0/src/libsbmlsim/copied_AST.h"
    "/home/bertrand/Soft/libsbmlsim-1.1.0/src/libsbmlsim/myCompartment.h"
    "/home/bertrand/Soft/libsbmlsim-1.1.0/src/libsbmlsim/dSFMT-params19937.h"
    "/home/bertrand/Soft/libsbmlsim-1.1.0/src/libsbmlsim/myInitialAssignment.h"
    "/home/bertrand/Soft/libsbmlsim-1.1.0/src/libsbmlsim/typedefs.h"
    "/home/bertrand/Soft/libsbmlsim-1.1.0/src/libsbmlsim/dSFMT-params.h"
    "/home/bertrand/Soft/libsbmlsim-1.1.0/src/libsbmlsim/boolean.h"
    "/home/bertrand/Soft/libsbmlsim-1.1.0/src/libsbmlsim/allocated_memory.h"
    "/home/bertrand/Soft/libsbmlsim-1.1.0/src/libsbmlsim/osarch.h"
    "/home/bertrand/Soft/libsbmlsim-1.1.0/src/libsbmlsim/myEventAssignment.h"
    "/home/bertrand/Soft/libsbmlsim-1.1.0/src/libsbmlsim/myRule.h"
    "/home/bertrand/Soft/libsbmlsim-1.1.0/src/libsbmlsim/common.h"
    "/home/bertrand/Soft/libsbmlsim-1.1.0/src/libsbmlsim/dSFMT.h"
    "/home/bertrand/Soft/libsbmlsim-1.1.0/src/libsbmlsim/math_private.h"
    "/home/bertrand/Soft/libsbmlsim-1.1.0/src/libsbmlsim/dSFMT-common.h"
    "/home/bertrand/Soft/libsbmlsim-1.1.0/src/libsbmlsim/libsbmlsim.h"
    "/home/bertrand/Soft/libsbmlsim-1.1.0/src/libsbmlsim/my_getopt.h"
    "/home/bertrand/Soft/libsbmlsim-1.1.0/src/libsbmlsim/version.h"
    "/home/bertrand/Soft/libsbmlsim-1.1.0/src/libsbmlsim/mySpeciesReference.h"
    "/home/bertrand/Soft/libsbmlsim-1.1.0/src/libsbmlsim/myParameter.h"
    "/home/bertrand/Soft/libsbmlsim-1.1.0/src/libsbmlsim/equation.h"
    "/home/bertrand/Soft/libsbmlsim-1.1.0/src/libsbmlsim/myDelay.h"
    )
ENDIF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")

IF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  FILE(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/libsbmlsim" TYPE FILE FILES
    "/home/bertrand/Soft/libsbmlsim-1.1.0/API.txt"
    "/home/bertrand/Soft/libsbmlsim-1.1.0/AUTHORS.txt"
    "/home/bertrand/Soft/libsbmlsim-1.1.0/COPYING.txt"
    "/home/bertrand/Soft/libsbmlsim-1.1.0/FUNDING.txt"
    "/home/bertrand/Soft/libsbmlsim-1.1.0/LICENSE.txt"
    "/home/bertrand/Soft/libsbmlsim-1.1.0/LICENSE-dSFMT.txt"
    "/home/bertrand/Soft/libsbmlsim-1.1.0/NEWS.txt"
    "/home/bertrand/Soft/libsbmlsim-1.1.0/README.txt"
    "/home/bertrand/Soft/libsbmlsim-1.1.0/VERSION.txt"
    )
ENDIF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")

IF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  FILE(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/libsbmlsim" TYPE FILE FILES
    "/home/bertrand/Soft/libsbmlsim-1.1.0/examples/sample.xml"
    "/home/bertrand/Soft/libsbmlsim-1.1.0/examples/sample.result"
    "/home/bertrand/Soft/libsbmlsim-1.1.0/examples/sample.plt"
    "/home/bertrand/Soft/libsbmlsim-1.1.0/examples/sample.pdf"
    )
ENDIF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")

IF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  FILE(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/libsbmlsim/c" TYPE FILE FILES
    "/home/bertrand/Soft/libsbmlsim-1.1.0/examples/c/test.c"
    "/home/bertrand/Soft/libsbmlsim-1.1.0/examples/c/Makefile"
    )
ENDIF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")

IF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  FILE(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/libsbmlsim/cpp" TYPE FILE FILES
    "/home/bertrand/Soft/libsbmlsim-1.1.0/examples/cpp/test.cpp"
    "/home/bertrand/Soft/libsbmlsim-1.1.0/examples/cpp/Makefile"
    )
ENDIF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")

IF(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for each subdirectory.
  INCLUDE("/home/bertrand/Soft/libsbmlsim-1.1.0/build/src/bindings/python/cmake_install.cmake")

ENDIF(NOT CMAKE_INSTALL_LOCAL_ONLY)

