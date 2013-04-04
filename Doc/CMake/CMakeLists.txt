# install stuff for cmake

install(FILES
    aspell.en.pws
    convert.sh
    doxygen2docbook.xsl
    FindDocBook.cmake
    fop.xconf
    indent.xsl
    logging.properties
    myhtml.xsl
    tidy.config
    UseDocBook.cmake
    xmldepend.xsl
  DESTINATION ${Documentation_INSTALL_CMAKE_DIR}
  COMPONENT CMakeModules)

# Format path in the html way. Needed by import tag to work with spaces
if(WIN32)
  set(TO_FORMAT
    Documentation_SOURCE_DIR
    DOCBOOK_XSL_DIRECTORY
    DOCBOOK_HTML_CHUNKFAST_XSL
    DOCBOOK_FO_XSL)

  foreach(var ${TO_FORMAT})
    set(${var}_OLD ${${var}})
    string(REGEX REPLACE " " "%20" ${var} "${${var}}")
  endforeach()
endif()

configure_file(
  ${CMAKE_CURRENT_SOURCE_DIR}/cosmodocbookcommon.fo.xsl.in
  ${CMAKE_CURRENT_BINARY_DIR}/cosmodocbookcommon.fo.xsl
  @ONLY)

configure_file(
  ${CMAKE_CURRENT_SOURCE_DIR}/cosmodocbookcommon.html.xsl.in
  ${CMAKE_CURRENT_BINARY_DIR}/cosmodocbookcommon.html.xsl
  @ONLY)

# Undo format
if(WIN32)
  foreach(var ${TO_FORMAT})
    set(${var} ${${var}_OLD})
  endforeach()
endif()
