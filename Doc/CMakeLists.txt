project(bpdDocumentation NONE)
cmake_minimum_required(VERSION 2.8)
set(CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/CMake")
set(DOCBOOK_SOURCE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/DocBook")
set(DOCBOOK_BINARY_DIR "${CMAKE_CURRENT_BINARY_DIR}/DocBook")
set(
  CMAKE_INSTALL_PREFIX "${CMAKE_CURRENT_BINARY_DIR}"
  CACHE PATH "BioPreDyn documentation install prefix" FORCE
  )

# --------------------------------------------------------------------------
find_package(DocBook REQUIRED)
include(${DocBook_USE_FILE})

configure_file(
  ${DOCBOOK_SOURCE_DIR}/bpddocbookcommon.fo.xsl.in
  ${DOCBOOK_BINARY_DIR}/bpddocbookcommon.fo.xsl
  @ONLY)

configure_file(
  ${DOCBOOK_SOURCE_DIR}/bpddocbookcommon.html.xsl.in
  ${DOCBOOK_BINARY_DIR}/bpddocbookcommon.html.xsl
  @ONLY)

add_subdirectory(IntegratedSoftwareSuite)
add_subdirectory(Prototype)

option( DOCUMENTATION_BUILD_TESTING "Build test suite." ON )
mark_as_advanced( DOCUMENTATION_BUILD_TESTING )
if( DOCUMENTATION_BUILD_TESTING )
  enable_testing()
  include(CTest)
  configure_file(${CMAKE_MODULE_PATH}/CTestCustom.ctest.in
    ${CMAKE_CURRENT_BINARY_DIR}/CTestCustom.ctest @ONLY)
  file(WRITE ${CMAKE_CURRENT_BINARY_DIR}/CTestCustom.cmake
    "INCLUDE(\"${CMAKE_CURRENT_BINARY_DIR}/CTestCustom.ctest\")\n")
  configure_file(${CMAKE_CURRENT_SOURCE_DIR}/CTestConfig.cmake
    ${CMAKE_CURRENT_BINARY_DIR}/CTestConfig.cmake
    COPY_ONLY)
endif()

generate_docbook_sitemap()
