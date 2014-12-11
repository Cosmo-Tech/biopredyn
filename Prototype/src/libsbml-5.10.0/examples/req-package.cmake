####################################################################
#
# SBML Required Elements package 
#
# $Author Lucian Smith$
# $Id$
# $HeadURL$
#

if (ENABLE_REQUIREDELEMENTS)
# add_subdirectory(c/req)
  add_subdirectory(c++/req)
  
  file(GLOB c_req_samples "${CMAKE_CURRENT_SOURCE_DIR}/c/req/*.c"
                         "${CMAKE_CURRENT_SOURCE_DIR}/c/req/*.h"
                         "${CMAKE_CURRENT_SOURCE_DIR}/c/req/README.txt")
  install(FILES ${c_req_samples} DESTINATION ${MISC_PREFIX}examples/c/req)

  file(GLOB cpp_req_samples "${CMAKE_CURRENT_SOURCE_DIR}/c++/req/*.c"
                         "${CMAKE_CURRENT_SOURCE_DIR}/c++/req/*.cpp"
                         "${CMAKE_CURRENT_SOURCE_DIR}/c++/req/*.h"
                         "${CMAKE_CURRENT_SOURCE_DIR}/c++/req/README.txt")
  install(FILES ${cpp_req_samples} DESTINATION ${MISC_PREFIX}examples/c++/req)
  
  if (WITH_PYTHON)
  # install python examples
  file(GLOB python_req_samples "${CMAKE_CURRENT_SOURCE_DIR}/python/req/*.py"
                           "${CMAKE_CURRENT_SOURCE_DIR}/python/req/README.txt")
  install(FILES ${python_req_samples} DESTINATION ${MISC_PREFIX}examples/python/req)
  endif()
  
endif(ENABLE_REQUIREDELEMENTS)
