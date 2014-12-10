cmake_minimum_required(VERSION 2.8)

set(SETUP_PY ${CMAKE_CURRENT_SOURCE_DIR}/setup.py)

add_subdirectory(cobrapy)

# biopredyn installation
install(
  CODE "execute_process(COMMAND ${PYTHON_EXECUTABLE} ${SETUP_PY} install --user WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR})"
  )
