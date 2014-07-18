cmake_minimum_required(VERSION 2.8)
project(BioPreDyn)

enable_testing()
include(CTest)

if(UNIX)
  if(CMAKE_SIZEOF_VOID_P EQUAL 8)
    set(CMAKE_LIBRARY_ARCHITECTURE "x86_64-linux-gnu" CACHE STRING "" FORCE)
  endif()
endif()

find_package(PythonInterp 2.7 REQUIRED)
find_package(PythonLibs 2.7 REQUIRED)

set(
  CMAKE_INSTALL_PREFIX "${CMAKE_BINARY_DIR}/install"
  CACHE PATH "BioPreDyn install prefix" FORCE
  )

# Determining Python user installation directory
execute_process(
  COMMAND "${PYTHON_EXECUTABLE}" -c "import sys;import site;sys.stdout.write(site.USER_SITE)"
  OUTPUT_VARIABLE PYTHON_USER_SITE)

set(PYTHON_PACKAGE_INSTALL_DIR)

set(
  PYTHON_PACKAGE_INSTALL_DIR "${PYTHON_USER_SITE}"
  CACHE PATH "Python libraries local install path" FORCE
  )

set(
  CMAKE_BUILD_TYPE "Release"
  CACHE PATH "CMake build type" FORCE
  )

if(NOT WIN32)
  option(BPD_GENERATE_DOXYGEN "Build the Doxygen documentation" ON)
  set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -fPIC")
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fPIC")
else()
  option(BPD_GENERATE_DOXYGEN "Build the Doxygen documentation" OFF)
endif()

option(WITH_PYTHON "Build Python wrappers for compiled libraries" ON)

IF(NOT DEFINED CMAKE_INSTALL_SYSTEM_RUNTIME_LIBS_NO_WARNINGS)
  SET(CMAKE_INSTALL_SYSTEM_RUNTIME_LIBS_NO_WARNINGS ON)
ENDIF()

IF(PYTHONINTERP_FOUND AND PYTHON_LIBRARIES)
  # Prototype software for testing (D7.2)
  add_subdirectory(Prototype)
ENDIF()
