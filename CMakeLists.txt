cmake_minimum_required(VERSION 2.8)
project(BioPreDyn NONE)

enable_testing()

include(CTest)
include(FindPythonInterp)
include(FindPythonLibs)

set(
  CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH}
  "${CMAKE_CURRENT_SOURCE_DIR}/Prototype/CMake/"
  )

set(
  CMAKE_INSTALL_PREFIX "${CMAKE_CURRENT_SOURCE_DIR}/Prototype/bin/"
  CACHE PATH "BioPreDyn install prefix" FORCE
  )

set(
  CMAKE_BUILD_TYPE "Release"
  )

option(BPD_GENERATE_DOXYGEN "Build the Doxygen documentation" OFF)
option(BPD_GENERATE_LIBBIOPREDYN "Build libBioPreDyn library" OFF)
option(WITH_PYTHON "Build Python wrappers for compiled libraries" ON)

if (PYTHONINTERP_FOUND AND PYTHON_LIBRARIES)
  # Prototype software for testing (D7.2)
  add_subdirectory(Prototype)
endif()
