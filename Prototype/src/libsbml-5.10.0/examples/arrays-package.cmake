####################################################################
#
# SBML Arrays package 
#
# $Author Lucian Smith$
# $Id$
# $HeadURL$
#

if (ENABLE_ARRAYS)
#        add_subdirectory(c/arrays)
  add_subdirectory(c++/arrays)
  
  file(GLOB c_arrays_samples "${CMAKE_CURRENT_SOURCE_DIR}/c/arrays/*.c"
                         "${CMAKE_CURRENT_SOURCE_DIR}/c/arrays/*.h"
                         "${CMAKE_CURRENT_SOURCE_DIR}/c/arrays/README.txt")
  install(FILES ${c_arrays_samples} DESTINATION ${MISC_PREFIX}examples/c/arrays)

  file(GLOB cpp_arrays_samples "${CMAKE_CURRENT_SOURCE_DIR}/c++/arrays/*.c"
                         "${CMAKE_CURRENT_SOURCE_DIR}/c++/arrays/*.cpp"
                         "${CMAKE_CURRENT_SOURCE_DIR}/c++/arrays/*.h"
                         "${CMAKE_CURRENT_SOURCE_DIR}/c++/arrays/README.txt")
  install(FILES ${cpp_arrays_samples} DESTINATION ${MISC_PREFIX}examples/c++/arrays)
  
  if (WITH_PYTHON)
  # install python examples
  file(GLOB python_arrays_samples "${CMAKE_CURRENT_SOURCE_DIR}/python/arrays/*.py"
                           "${CMAKE_CURRENT_SOURCE_DIR}/python/arrays/README.txt")
  install(FILES ${python_arrays_samples} DESTINATION ${MISC_PREFIX}examples/python/arrays)
  endif()
  
endif(ENABLE_ARRAYS)
