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
  CMAKE_INSTALL_PREFIX "${CMAKE_BINARY_DIR}/install/"
  CACHE PATH "BioPreDyn install prefix" FORCE
  )

set(
  CMAKE_BUILD_TYPE "Release"
  )

if(NOT WIN32)
  option(BPD_GENERATE_DOXYGEN "Build the Doxygen documentation" ON)
else()
  option(BPD_GENERATE_DOXYGEN "Build the Doxygen documentation" OFF)
endif()

set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -fPIC")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fPIC")

option(BPD_GENERATE_LIBBIOPREDYN "Build libBioPreDyn library" OFF)
option(WITH_PYTHON "Build Python wrappers for compiled libraries" ON)

if (PYTHONINTERP_FOUND AND PYTHON_LIBRARIES)
  # Prototype software for testing (D7.2)
  add_subdirectory(Prototype)
endif()
