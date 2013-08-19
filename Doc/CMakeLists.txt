project(Documentation NONE)
cmake_minimum_required(VERSION 2.8) # get_filename_component unknown component REALPATH
set(Documentation_CMAKE_DIR "${Documentation_SOURCE_DIR}/CMake" CACHE INTERNAL "")
set(CMAKE_MODULE_PATH "${Documentation_CMAKE_DIR}")

# --------------------------------------------------------------------------
# Configure the export configuration

# You will also need to define a value for the following variables:
# Documentation_INSTALL_DATA_DIR         - share dir (say, examples, data, etc)
# Documentation_INSTALL_CMAKE_DIR        - cmake files (cmake)

# --------------------------------------------------------------------------
# Install directories

set(documentation_directory "Documentation")
if(NOT Documentation_INSTALL_DATA_DIR)
  set(Documentation_INSTALL_DATA_DIR "share/${documentation_directory}")
endif()

if(NOT Documentation_INSTALL_CMAKE_DIR)
  set(Documentation_INSTALL_CMAKE_DIR "lib/${documentation_directory}")
endif()

# --------------------------------------------------------------------------
if(WIN32)
  find_package(csmExternals REQUIRED)
  include(${CSMEXTERNALS_USE_FILE})
endif()

# --------------------------------------------------------------------------
find_package(DocBook REQUIRED)
include(${DocBook_USE_FILE})

add_subdirectory(CMake)
add_subdirectory(IntegratedSoftwareSuite)
add_subdirectory(Prototype)

option( DOCUMENTATION_BUILD_TESTING "Build test suite." ON )
mark_as_advanced(DOCUMENTATION_BUILD_TESTING)
if( DOCUMENTATION_BUILD_TESTING )
  # This is needed to be able to drive build process from CTest
  enable_testing()
  include(CTest)
  mark_as_advanced(DART_TESTING_TIMEOUT BUILD_TESTING)
  configure_file(${Documentation_CMAKE_DIR}/CTestCustom.ctest.in
    ${Documentation_BINARY_DIR}/CTestCustom.ctest @ONLY)
  file(WRITE ${Documentation_BINARY_DIR}/CTestCustom.cmake
    "INCLUDE(\"${Documentation_BINARY_DIR}/CTestCustom.ctest\")\n")
  configure_file(${CMAKE_CURRENT_SOURCE_DIR}/CTestConfig.cmake
    ${CMAKE_CURRENT_BINARY_DIR}/CTestConfig.cmake
    COPY_ONLY)
endif()

# This function need to be called after all `ADD_DOCBOOK`
generate_docbook_sitemap()