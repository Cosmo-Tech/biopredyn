cmake_minimum_required(VERSION 2.8)
project(libbiopredyn CXX)

FIND_PACKAGE(PythonLibs)
FIND_PACKAGE(XSD REQUIRED)
FIND_PACKAGE(SWIG REQUIRED)

INCLUDE(${SWIG_USE_FILE})
INCLUDE_DIRECTORIES(${PYTHON_INCLUDE_PATH})
INCLUDE_DIRECTORIES(${CMAKE_CURRENT_SOURCE_DIR})
INCLUDE_DIRECTORIES(${XSD_INCLUDE_DIR})

ADD_CUSTOM_COMMAND( 
    OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/libbiopredyn_wrap.cpp
    COMMAND "${SWIG_EXECUTABLE}"
    ARGS    -I${CMAKE_SOURCE_DIR}/
            -I${CMAKE_BINARY_DIR}/
            -I${CMAKE_CURRENT_SOURCE_DIR}
            -I${LIBSBML_INCLUDE_DIR}/
            -c++
            -python     
            ${SWIG_EXTRA_FLAGS}      
            ${SWIG_EXTRA_ARGS}       
            -o ${CMAKE_CURRENT_BINARY_DIR}/libbiopredyn_wrap.cpp 
            ${CMAKE_CURRENT_SOURCE_DIR}/biopredyn.i
    COMMENT "Swig Python source") 

add_custom_target(biopredyn_binding_python_swig ALL DEPENDS ${CMAKE_CURRENT_BINARY_DIR}/libbiopredyn_wrap.cpp)

add_library(biopredyn_binding_python_lib SHARED libbiopredyn_wrap.cpp)
add_dependencies( biopredyn_binding_python_lib biopredyn_binding_python_swig) 

set_target_properties (biopredyn_binding_python_lib PROPERTIES OUTPUT_NAME "_libbiopredyn")
if (UNIX)
    set_target_properties (biopredyn_binding_python_lib PROPERTIES PREFIX "")
    set_target_properties (biopredyn_binding_python_lib PROPERTIES SUFFIX ".so")
else()      
    if (CYGWIN)
        set_target_properties (biopredyn_binding_python_lib PROPERTIES PREFIX "")
        set_target_properties (biopredyn_binding_python_lib PROPERTIES SUFFIX ".dll")
    else()
        set_target_properties (biopredyn_binding_python_lib PROPERTIES SUFFIX ".pyd")    
    endif()
endif()

target_link_libraries(biopredyn_binding_python_lib ${PYTHON_LIBRARIES})

# Wrappers installation in BioPreDyn package
set(PYTHON_PACKAGE_INSTALL_DIR)
if (UNIX OR CYGWIN) 
  execute_process(COMMAND "${PYTHON_EXECUTABLE}" -c "import sys;import platform; sys.stdout.write(platform.python_version()[:3])"
    OUTPUT_VARIABLE PYTHON_VERSION)
  set(PYTHON_PACKAGE_INSTALL_DIR ${CMAKE_INSTALL_LIBDIR}/python${PYTHON_VERSION}/site-packages)
else()
  set(PYTHON_PACKAGE_INSTALL_DIR ${MISC_PREFIX}bindings/python)
endif()

INSTALL(TARGETS biopredyn_binding_python_lib DESTINATION ${PYTHON_PACKAGE_INSTALL_DIR}/libbiopredyn )

file(WRITE "${CMAKE_CURRENT_BINARY_DIR}/libbiopredyn.pth" "libbiopredyn\n")
INSTALL(FILES ${CMAKE_CURRENT_BINARY_DIR}/libbiopredyn.pth  DESTINATION ${PYTHON_PACKAGE_INSTALL_DIR})
INSTALL(FILES ${CMAKE_CURRENT_BINARY_DIR}/libbiopredyn.py  DESTINATION ${PYTHON_PACKAGE_INSTALL_DIR}/libbiopredyn )