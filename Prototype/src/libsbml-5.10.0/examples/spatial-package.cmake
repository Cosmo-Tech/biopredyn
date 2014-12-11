####################################################################
#
# SBML Spatial Processes package 
#
# $Author Lucian Smith$
# $Id$
# $HeadURL$
#

if (ENABLE_SPATIAL)
#  add_subdirectory(c/spatial)
  add_subdirectory(c++/spatial)
  
  file(GLOB c_spatial_samples "${CMAKE_CURRENT_SOURCE_DIR}/c/spatial/*.c"
                         "${CMAKE_CURRENT_SOURCE_DIR}/c/spatial/*.h"
                         "${CMAKE_CURRENT_SOURCE_DIR}/c/spatial/README.txt")
  install(FILES ${c_spatial_samples} DESTINATION ${MISC_PREFIX}examples/c/spatial)

  file(GLOB cpp_spatial_samples "${CMAKE_CURRENT_SOURCE_DIR}/c++/spatial/*.c"
                         "${CMAKE_CURRENT_SOURCE_DIR}/c++/spatial/*.cpp"
                         "${CMAKE_CURRENT_SOURCE_DIR}/c++/spatial/*.h"
                         "${CMAKE_CURRENT_SOURCE_DIR}/c++/spatial/README.txt")
  install(FILES ${cpp_spatial_samples} DESTINATION ${MISC_PREFIX}examples/c++/spatial)
  
  if (WITH_PYTHON)
  # install python examples
  file(GLOB python_spatial_samples "${CMAKE_CURRENT_SOURCE_DIR}/python/spatial/*.py"
                           "${CMAKE_CURRENT_SOURCE_DIR}/python/spatial/README.txt")
  install(FILES ${python_spatial_samples} DESTINATION ${MISC_PREFIX}examples/python/spatial)
  endif()
  
endif(ENABLE_SPATIAL)
