###############################################################################
#
# Description       : CMake build script for libNUML examples
# Original author(s): Joseph Olufemi Dada <joseph.dada@@manchester.ac.uk>
# Organization      : The University of Manchester
#
# This file is part of libNUML.  Please visit http://numl.org for more
# information about NUML, and the latest version of libNUML.
#
# Copyright (c) 2013, 
# All rights reserved.
#
#
###############################################################################

# only compile examples if specified, but always copy samples
if(WITH_EXAMPLES)

#add_subdirectory(c)
add_subdirectory(c++)

endif(WITH_EXAMPLES)



# the remaining language bindings do not need to be compiled in order to run. 

# Now we just have to select files for installation# 
install(FILES README.md DESTINATION ${MISC_PREFIX}examples)

## install c examples
file(GLOB c_samples "${CMAKE_CURRENT_SOURCE_DIR}/c/*.c"
					 "${CMAKE_CURRENT_SOURCE_DIR}/c/README.md"
					 "${CMAKE_CURRENT_SOURCE_DIR}/c/*.h")
install(FILES ${c_samples} DESTINATION ${MISC_PREFIX}examples/c)
#
# install c++ examples
file(GLOB cpp_samples "${CMAKE_CURRENT_SOURCE_DIR}/c++/*.c"
					 "${CMAKE_CURRENT_SOURCE_DIR}/c++/README.md"
					 "${CMAKE_CURRENT_SOURCE_DIR}/c++/*.cpp"
					 "${CMAKE_CURRENT_SOURCE_DIR}/c++/*.h")
install(FILES ${cpp_samples} DESTINATION ${MISC_PREFIX}examples/c++)

if (WITH_PYTHON)
# install python examples
file(GLOB python_samples "${CMAKE_CURRENT_SOURCE_DIR}/python/*.py"
					 "${CMAKE_CURRENT_SOURCE_DIR}/python/README.md")
install(FILES ${python_samples} DESTINATION ${MISC_PREFIX}examples/python)
endif()


# install example-data

file(GLOB example_data "${CMAKE_CURRENT_SOURCE_DIR}/example-data/*.xml")
install(FILES ${example_data} DESTINATION ${MISC_PREFIX}examples/example-data)

