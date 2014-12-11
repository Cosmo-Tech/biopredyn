####################################################################
#
# SBML Multi package 
#
# $Author Lucian Smith$
# $Id$
# $HeadURL$
#

if (ENABLE_MULTI)
  # add_subdirectory(c/fbc)
  add_subdirectory(c++/multi)
  
  file(GLOB c_multi_samples "${CMAKE_CURRENT_SOURCE_DIR}/c/multi/*.c"
                         "${CMAKE_CURRENT_SOURCE_DIR}/c/multi/*.h"
                         "${CMAKE_CURRENT_SOURCE_DIR}/c/multi/README.txt")
  install(FILES ${c_multi_samples} DESTINATION ${MISC_PREFIX}examples/c/multi)

  file(GLOB cpp_multi_samples "${CMAKE_CURRENT_SOURCE_DIR}/c++/multi/*.c"
                         "${CMAKE_CURRENT_SOURCE_DIR}/c++/multi/*.cpp"
                         "${CMAKE_CURRENT_SOURCE_DIR}/c++/multi/*.h"
                         "${CMAKE_CURRENT_SOURCE_DIR}/c++/multi/README.txt")
  install(FILES ${cpp_multi_samples} DESTINATION ${MISC_PREFIX}examples/c++/multi)
  
  if (WITH_PYTHON)
  # install python examples
  file(GLOB python_multi_samples "${CMAKE_CURRENT_SOURCE_DIR}/python/multi/*.py"
                           "${CMAKE_CURRENT_SOURCE_DIR}/python/multi/README.txt")
  install(FILES ${python_multi_samples} DESTINATION ${MISC_PREFIX}examples/python/multi)
  endif()
  
endif(ENABLE_MULTI)
