cmake_minimum_required(VERSION 2.8)

set(SETUP_PY_IN ${CMAKE_CURRENT_SOURCE_DIR}/setup.py.in)
set(SETUP_PY ${CMAKE_CURRENT_BINARY_DIR}/setup.py)
#set(MAIN_PY_IN ${CMAKE_CURRENT_SOURCE_DIR}/biopredyn/main.py.in)
#set(MAIN_PY ${CMAKE_BINARY_DIR}/build/main.py)
set(DEPS ${CMAKE_CURRENT_SOURCE_DIR}/biopredyn/__init__.py)
set(OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/build/timestamp)

configure_file(${SETUP_PY_IN} ${SETUP_PY})
#configure_file(${MAIN_PY_IN} ${MAIN_PY})

add_custom_command(OUTPUT ${OUTPUT}
  COMMAND ${PYTHON_EXECUTABLE} ${SETUP_PY} build
  COMMAND ${CMAKE_COMMAND} -E touch ${OUTPUT}
  DEPENDS ${DEPS})

add_custom_target(bpd_engine ALL DEPENDS ${OUTPUT})

# Testing installation
add_test(BioPreDynPackageInstall ${CMAKE_COMMAND} -P ${CMAKE_BINARY_DIR}/cmake_install.cmake)

install(
  CODE "execute_process(COMMAND ${PYTHON_EXECUTABLE} ${SETUP_PY} install --user)"
  )