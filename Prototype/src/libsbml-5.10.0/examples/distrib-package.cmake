####################################################################
#
# SBML Distributions package 
#
# $Author Lucian Smith$
# $Id$
# $HeadURL$
#

if (ENABLE_DISTRIB)
#  add_subdirectory(c/distrib)
add_subdirectory(c++/distrib)

  file(GLOB c_distrib_samples "${CMAKE_CURRENT_SOURCE_DIR}/c/distrib/*.c"
                         "${CMAKE_CURRENT_SOURCE_DIR}/c/distrib/*.h"
                         "${CMAKE_CURRENT_SOURCE_DIR}/c/distrib/README.txt")
  install(FILES ${c_distrib_samples} DESTINATION ${MISC_PREFIX}examples/c/distrib)

  file(GLOB cpp_distrib_samples "${CMAKE_CURRENT_SOURCE_DIR}/c++/distrib/*.c"
                         "${CMAKE_CURRENT_SOURCE_DIR}/c++/distrib/*.cpp"
                         "${CMAKE_CURRENT_SOURCE_DIR}/c++/distrib/*.h"
                         "${CMAKE_CURRENT_SOURCE_DIR}/c++/distrib/README.txt")
  install(FILES ${cpp_distrib_samples} DESTINATION ${MISC_PREFIX}examples/c++/distrib)
  
  if (WITH_PYTHON)
  # install python examples
  file(GLOB python_distrib_samples "${CMAKE_CURRENT_SOURCE_DIR}/python/distrib/*.py"
                           "${CMAKE_CURRENT_SOURCE_DIR}/python/distrib/README.txt")
  install(FILES ${python_distrib_samples} DESTINATION ${MISC_PREFIX}examples/python/distrib)
  endif()
   
endif(ENABLE_DISTRIB)
