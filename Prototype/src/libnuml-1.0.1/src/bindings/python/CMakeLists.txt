###############################################################################
#
# Description       : CMake build script for libNUML Python bindings
# Original author(s): Joseph O. Dada <joseph.dada@manchester.ac.uk>
# Organization      : University of Manchester
#
# This file is part of libNUML.  Please visit http://numl-ml.org for more
# information about NUML, and the latest version of libNUML.
#
# Copyright (c) 2013, University of Manchester  
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met: 
# 
#
###############################################################################

find_package(SWIG REQUIRED)
include(${SWIG_USE_FILE})
include(FindPythonLibs)
include(FindPythonInterp)


####################################################################
#
# determine local dependencies, so as to re-swig if one of them changed
# 

file(GLOB SWIG_DEPENDENCIES 
	${CMAKE_CURRENT_SOURCE_DIR}/*.i 
	${CMAKE_CURRENT_SOURCE_DIR}/*.h 
	${CMAKE_CURRENT_SOURCE_DIR}/*.cpp
	${CMAKE_CURRENT_SOURCE_DIR}/../swig/*.i
	${CMAKE_CURRENT_SOURCE_DIR}/../swig/*.h
	)

#
# Remove SWIG wrappers if requested
#
if (LIBNUML_REMOVE_WRAPPERS)
  foreach(file 
    ${CMAKE_CURRENT_BINARY_DIR}/libnuml_wrap.cpp
  )
    if (EXISTS ${file})
      FILE(REMOVE ${file})
    endif()
  endforeach()
endif(LIBNUML_REMOVE_WRAPPERS)


set(SWIG_EXTRA_FLAGS -DSWIGEXPORT -DLIBSBML_CPP_NAMESPACE_BEGIN -DLIBSBML_CPP_NAMESPACE_END)
if(NOT UNIX)
	set(SWIG_EXTRA_FLAGS ${SWIG_EXTRA_FLAGS} -DSWIGWIN -DSWIG_CSHARP_NO_WSTRING_HELPER )
endif()

ADD_CUSTOM_COMMAND(	
    OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/libnuml_wrap.cpp
    COMMAND "${SWIG_EXECUTABLE}"
    ARGS	-I${CMAKE_CURRENT_SOURCE_DIR}/../swig/
            -I${CMAKE_CURRENT_SOURCE_DIR}/../../
			-I${CMAKE_SOURCE_DIR}/
			-I${CMAKE_BINARY_DIR}/
			-I${CMAKE_SOURCE_DIR}/src
			-I${CMAKE_SOURCE_DIR}/include
			-I${CMAKE_SOURCE_DIR}/numl
			-I${CMAKE_CURRENT_SOURCE_DIR}
			-I${LIBSBML_INCLUDE_DIR}/
			-c++
			-python		
			${SWIG_EXTRA_FLAGS}		 
			${SWIG_EXTRA_ARGS}		 
			-o ${CMAKE_CURRENT_BINARY_DIR}/libnuml_wrap.cpp 
			${CMAKE_CURRENT_SOURCE_DIR}/libnuml.i
	DEPENDS local.i local.cpp local-contrib.i
    COMMENT "Swig Python source") 

add_custom_target(numl_binding_python_swig ALL DEPENDS ${CMAKE_CURRENT_BINARY_DIR}/libnuml_wrap.cpp)
	
####################################################################
#
# Build native library
#

include_directories(${CMAKE_CURRENT_SOURCE_DIR})
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/../swig)
include_directories(${LIBSBML_INCLUDE_DIR})
include_directories(BEFORE ${CMAKE_SOURCE_DIR}/src)
include_directories(BEFORE ${CMAKE_SOURCE_DIR})
include_directories(BEFORE ${CMAKE_BINARY_DIR})
add_definitions(-DLIBNUML_STATIC)
include_directories(${PYTHON_INCLUDE_DIRS})
if (EXTRA_INCLUDE_DIRS) 
 include_directories(${EXTRA_INCLUDE_DIRS})
endif(EXTRA_INCLUDE_DIRS)

if (MSVC)
  # the build fails when compiled with packages as the object file is too 
  # big adding the big flag makes it work!
  add_definitions(/bigobj)
endif(MSVC)

# BioPreDyn patch - Changed name of the binding targets so that they do not
# overlap with the the ones from libSEDML and libSBML
add_library(numl_binding_python_lib SHARED libnuml_wrap.cpp)
add_dependencies( numl_binding_python_lib numl_binding_python_swig) 

set_target_properties (numl_binding_python_lib PROPERTIES OUTPUT_NAME "_libnuml")
if (UNIX)
	set_target_properties (numl_binding_python_lib PROPERTIES PREFIX "")
	set_target_properties (numl_binding_python_lib PROPERTIES SUFFIX ".so")
else()		
	if (CYGWIN)
		set_target_properties (numl_binding_python_lib PROPERTIES PREFIX "")
		set_target_properties (numl_binding_python_lib PROPERTIES SUFFIX ".dll")
	else()
		set_target_properties (numl_binding_python_lib PROPERTIES SUFFIX ".pyd")	
	endif()
endif()

# BioPreDyn patch - linking libNuMLwrappers with libSBML wrappers
target_link_libraries(numl_binding_python_lib sbml_binding_python_lib ${LIBNUML_PREFIX}-static ${PYTHON_LIBRARIES})

# BioPreDyn patch - removed PYTHON_PACKAGE_INSTALL_DIR determination
INSTALL(TARGETS numl_binding_python_lib DESTINATION ${PYTHON_PACKAGE_INSTALL_DIR}/libnuml )

file(WRITE "${CMAKE_CURRENT_BINARY_DIR}/libnuml.pth" "libnuml\n")
INSTALL(FILES ${CMAKE_CURRENT_BINARY_DIR}/libnuml.pth  DESTINATION ${PYTHON_PACKAGE_INSTALL_DIR})
INSTALL(FILES ${CMAKE_CURRENT_BINARY_DIR}/libnuml.py  DESTINATION ${PYTHON_PACKAGE_INSTALL_DIR}/libnuml )
