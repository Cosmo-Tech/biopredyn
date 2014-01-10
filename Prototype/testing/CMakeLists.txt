# First test: opens a file and test whether it is SBML compliant
add_test(SBMLComplianceTest ${PYTHON_EXECUTABLE}
  ${CMAKE_CURRENT_SOURCE_DIR}/test.py
  ${CMAKE_CURRENT_SOURCE_DIR}/../data/FEBS.xml --sbml)

# Second test: opens a file, test whether it is SED-ML compliant, execute it
add_test(SedMLComplianceTest ${PYTHON_EXECUTABLE}
  ${CMAKE_CURRENT_SOURCE_DIR}/test.py
  ${CMAKE_CURRENT_SOURCE_DIR}/../data/FEBS_UniformTimeCourse.xml --sedml)

# Third test: opens a NuML result file and plot its content with matplotlib.
add_test(NuMLFileImportTest ${PYTHON_EXECUTABLE}
  ${CMAKE_CURRENT_SOURCE_DIR}/test.py
  ${CMAKE_CURRENT_SOURCE_DIR}/../data/FEBS_numerical_data.xml --numl)