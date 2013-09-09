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

option(BPD_GENERATE_DOXYGEN "Build the Doxygen documentation" ON)
option(BPD_GENERATE_LIBBIOPREDYN "Build libBioPreDyn library" ON)

if (BPD_GENERATE_LIBBIOPREDYN)
  # Parsing library for biopredyn.xsd based XML files
  add_subdirectory(libBioPreDyn)
endif()

if (PYTHONINTERP_FOUND AND PYTHON_LIBRARIES)
  # Prototype software for testing (D7.2)
  add_subdirectory(Prototype)
endif()