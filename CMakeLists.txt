cmake_minimum_required(VERSION 2.8)
project(BioPreDyn NONE)

enable_testing()

include(CTest)
include(FindPythonInterp)
include(FindPythonLibs)

if (PYTHONINTERP_FOUND AND PYTHON_LIBRARIES)
  # Prototype software for testing (D7.2)
  add_subdirectory(Prototype)
endif()