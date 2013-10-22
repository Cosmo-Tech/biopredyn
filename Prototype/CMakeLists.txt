set(PACKAGE_VERSION 0.1)

add_subdirectory(src)
add_subdirectory(python)

# doxygen generation
if (BPD_GENERATE_DOXYGEN)
  add_subdirectory(doxygen)
endif()

# First test: opens a file and test whether it is SBML compliant
add_test(SBMLComplianceTest ${PYTHON_EXECUTABLE}
  ${CMAKE_CURRENT_SOURCE_DIR}/python/biopredyn/main.py
  ${CMAKE_CURRENT_SOURCE_DIR}/data/FEBS.xml --sbml)

# Second test: opens a file, test whether it is SED-ML compliant, execute it
add_test(SedMLComplianceTest ${PYTHON_EXECUTABLE}
  ${CMAKE_CURRENT_SOURCE_DIR}/python/biopredyn/main.py
  ${CMAKE_CURRENT_SOURCE_DIR}/data/FEBS_UniformTimeCourse.xml --sedml)