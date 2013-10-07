cmake_minimum_required(VERSION 2.8)

# First test: opens a file and test whether it is SBML compliant
add_test(SBMLComplianceTest ${PYTHON_EXECUTABLE}
  ${CMAKE_CURRENT_SOURCE_DIR}/main.py
  ${CMAKE_CURRENT_SOURCE_DIR}/Data/FEBS.xml --sbml)

# Second test: opens a file, test whether it is SED-ML compliant, execute it
add_test(SedMLComplianceTest ${PYTHON_EXECUTABLE}
  ${CMAKE_CURRENT_SOURCE_DIR}/main.py
  ${CMAKE_CURRENT_SOURCE_DIR}/Data/FEBS_UniformTimeCourse.xml --sedml)

# doxygen generation
if (BPD_GENERATE_DOXYGEN)
  add_subdirectory(Doxygen)
endif()