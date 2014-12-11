####################################################################
#
# SBML Rendering package 
#
# $Author Lucian Smith$
# $Id$
# $HeadURL$
#

if (ENABLE_RENDER)
#        add_subdirectory(c/render)
  add_subdirectory(c++/render)
  
  file(GLOB c_render_samples "${CMAKE_CURRENT_SOURCE_DIR}/c/render/*.c"
                         "${CMAKE_CURRENT_SOURCE_DIR}/c/render/*.h"
                         "${CMAKE_CURRENT_SOURCE_DIR}/c/render/README.txt")
  install(FILES ${c_render_samples} DESTINATION ${MISC_PREFIX}examples/c/render)

  file(GLOB cpp_render_samples "${CMAKE_CURRENT_SOURCE_DIR}/c++/render/*.c"
                         "${CMAKE_CURRENT_SOURCE_DIR}/c++/render/*.cpp"
                         "${CMAKE_CURRENT_SOURCE_DIR}/c++/render/*.h"
                         "${CMAKE_CURRENT_SOURCE_DIR}/c++/render/README.txt")
  install(FILES ${cpp_render_samples} DESTINATION ${MISC_PREFIX}examples/c++/render)
  
  if (WITH_PYTHON)
  # install python examples
  file(GLOB python_render_samples "${CMAKE_CURRENT_SOURCE_DIR}/python/render/*.py"
                           "${CMAKE_CURRENT_SOURCE_DIR}/python/render/README.txt")
  install(FILES ${python_render_samples} DESTINATION ${MISC_PREFIX}examples/python/render)
  endif()
  
endif(ENABLE_RENDER)
