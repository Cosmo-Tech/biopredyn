# First test: opens a file and test whether it is SBML compliant
add_test(SBMLComplianceTest ${PYTHON_EXECUTABLE}
  ${CMAKE_CURRENT_SOURCE_DIR}/main.py
  ${CMAKE_CURRENT_SOURCE_DIR}/Data/FEBS.xml --sbml)