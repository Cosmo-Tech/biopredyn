####################################################################
#
# SBML Groups package 
#
# $Author Lucian Smith$
# $Id$
# $HeadURL$
#

if (ENABLE_GROUPS)
#        add_subdirectory(c/groups)
  add_subdirectory(c++/groups)
  
  
  file(GLOB c_groups_samples "${CMAKE_CURRENT_SOURCE_DIR}/c/groups/*.c"
                         "${CMAKE_CURRENT_SOURCE_DIR}/c/groups/*.h"
                         "${CMAKE_CURRENT_SOURCE_DIR}/c/groups/README.txt")
  install(FILES ${c_groups_samples} DESTINATION ${MISC_PREFIX}examples/c/groups)

  file(GLOB cpp_groups_samples "${CMAKE_CURRENT_SOURCE_DIR}/c++/groups/*.c"
                         "${CMAKE_CURRENT_SOURCE_DIR}/c++/groups/*.cpp"
                         "${CMAKE_CURRENT_SOURCE_DIR}/c++/groups/*.h"
                         "${CMAKE_CURRENT_SOURCE_DIR}/c++/groups/README.txt")
  install(FILES ${cpp_groups_samples} DESTINATION ${MISC_PREFIX}examples/c++/groups)
  
  if (WITH_PYTHON)
  # install python examples
  file(GLOB python_groups_samples "${CMAKE_CURRENT_SOURCE_DIR}/python/groups/*.py"
                           "${CMAKE_CURRENT_SOURCE_DIR}/python/groups/README.txt")
  install(FILES ${python_groups_samples} DESTINATION ${MISC_PREFIX}examples/python/groups)
  endif()
  
endif(ENABLE_GROUPS)
