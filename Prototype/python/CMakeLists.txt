cmake_minimum_required(VERSION 2.8)

set(SETUP_PY_IN ${CMAKE_CURRENT_SOURCE_DIR}/setup.py.in)
set(SETUP_PY ${CMAKE_CURRENT_BINARY_DIR}/setup.py)
set(DEPS ${CMAKE_CURRENT_SOURCE_DIR}/biopredyn/__init__.py)
set(OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/build/timestamp)

configure_file(${SETUP_PY_IN} ${SETUP_PY})

add_custom_command(OUTPUT ${OUTPUT}
  COMMAND ${PYTHON_EXECUTABLE} ${SETUP_PY} build
  COMMAND ${CMAKE_COMMAND} -E touch ${OUTPUT}
  DEPENDS ${DEPS})

add_custom_target(target ALL DEPENDS ${OUTPUT})

install(
  CODE "execute_process(COMMAND ${PYTHON_EXECUTABLE} ${SETUP_PY} install)"
  )

# First test: opens a file and test whether it is SBML compliant
add_test(SBMLComplianceTest ${PYTHON_EXECUTABLE}
  ${CMAKE_CURRENT_SOURCE_DIR}/biopredyn/main.py
  ${CMAKE_CURRENT_SOURCE_DIR}/../data/FEBS.xml --sbml)

# Second test: opens a file, test whether it is SED-ML compliant, execute it
add_test(SedMLComplianceTest ${PYTHON_EXECUTABLE}
  ${CMAKE_CURRENT_SOURCE_DIR}/biopredyn/main.py
  ${CMAKE_CURRENT_SOURCE_DIR}/../data/FEBS_UniformTimeCourse.xml --sedml)