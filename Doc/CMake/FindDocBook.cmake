# - Find DocBook
# This module finds an installed DocBook.  It sets the following variables:
# DOCBOOK_BUILD_HTML        = option whether or not to build HTML output
# DOCBOOK_BUILD_PDF         = option whether or not to build PDF output
# DOCBOOK_BUILD_VALIDATION  = option whether or not to add DTD validation
#                             on the docbook file
# DOCBOOK_BUILD_SPELLCHECK  = option whether or not to add aspell check

# We need to locate ourself. See xmldepend.xsl file
get_filename_component(
  DocBook_CURRENT_LIST_DIR ${CMAKE_CURRENT_LIST_FILE} PATH)

# This option allows generation of HTML pages
option(DOCBOOK_BUILD_HTML "Build HTML?" ON)

# This option allows generation of XHTML pages
#option(DOCBOOK_BUILD_XHTML "Build XHTML?" OFF)
#mark_as_advanced(DOCBOOK_BUILD_XHTML)

# This option allows generation of PDF document
option(DOCBOOK_BUILD_PDF "Build PDF?" OFF)

# This option allows validation of DTD of docbook document (advanced user)
option(DOCBOOK_BUILD_VALIDATION "Build Validation Target?" OFF)

option(DOCBOOK_BUILD_SPELLCHECK "Build Spell Check Target? (Experimental)" OFF)
mark_as_advanced(DOCBOOK_BUILD_SPELLCHECK)

option(DOCBOOK_USE_SYNTAX_HIGHLIGHTING "Build Syntax Highlighting ? (Experimental)" OFF)
mark_as_advanced(DOCBOOK_USE_SYNTAX_HIGHLIGHTING)

include(FindPackageHandleStandardArgs)
if(DOCBOOK_USE_SYNTAX_HIGHLIGHTING)
  # xslthl only works with Java XSLT engine. We'll use SAXON in this case.
  set(DOCBOOK_USE_SAXON 1)
  find_package(Java REQUIRED)
  # apt-get install libsaxon-java
  find_file(SAXON_JAR saxon.jar
    /usr/share/java/
    )
  # http://www.sagehill.net/docbookxsl/InstallingAProcessor.html#SaxonExtensions
  # http://wiki.docbook.org/topic/DocBookXsltExtensions
  # apt-get install docbook-xsl-saxon
  find_file(DOCBOOK_XSL_SAXON_JAR docbook-xsl-saxon.jar
    /usr/share/java/
    )
  # http://www.sagehill.net/docbookxsl/SyntaxHighlighting.html
  # apt-get install libxslthl-java
  find_file(XSLTHL_JAR xslthl.jar
    /usr/share/java/
    )
  find_file(XSLTHL_CONFIG_XML xslthl-config.xml
    /usr/share/xslthl/highlighters/
    )
  # http://www.sagehill.net/docbookxsl/UseCatalog.html
  # apt-get install libxml-commons-resolver1.1-java
  # UBUNTU has renamed xml-commons-resolver-1.1.jar into
  # xml-resolver.jar. Adding xml-resolver.jar to the list of files to
  # search for.
  find_file(XML_COMMONS_RESOLVER_JAR NAMES xml-commons-resolver-1.1.jar xml-resolver.jar
    HINTS /usr/share/java/
    )
  # WARNING: The following file has a special option:
  # prefer=[public|system]
  # one should make sure to use prefer=public to match with xsltproc behavior.
  find_path(XML_COMMONS_RESOLVER_CATALOGMANAGER_PROPERTIES_PATH
    CatalogManager.properties
    /etc/xml/resolver/
    )
  mark_as_advanced(
    SAXON_JAR
    DOCBOOK_XSL_SAXON_JAR
    XSLTHL_JAR
    XSLTHL_CONFIG_XML
    XML_COMMONS_RESOLVER_JAR
    XML_COMMONS_RESOLVER_CATALOGMANAGER_PROPERTIES_PATH
  )
  find_package_handle_standard_args(DocBook
    "DocBook/Saxon could not be found"
    SAXON_JAR
    DOCBOOK_XSL_SAXON_JAR
    XSLTHL_JAR
    XSLTHL_CONFIG_XML
    XML_COMMONS_RESOLVER_JAR
    XML_COMMONS_RESOLVER_CATALOGMANAGER_PROPERTIES_PATH
    )
endif(DOCBOOK_USE_SYNTAX_HIGHLIGHTING)

if(DOCBOOK_BUILD_HTML)
  # apt-get install xsltproc
  find_program(XSLTPROC_EXECUTABLE xsltproc)
  find_path(DOCBOOK_HTML_XSL_DIRECTORY docbook.xsl
    /usr/share/xml/docbook/stylesheet/docbook-xsl/html/
    # I know this distro customization sucks but the following line is for
    # Fedora12 to work (rpm package is declined with the version number i.e.
    # docbook-style-xsl-1.75.2-4.fc12.noarch):
    /usr/share/sgml/docbook/xsl-stylesheets-1.75.2/html/
    # ubuntu
    /usr/share/xml/docbook/stylesheet/nwalsh/html/
    # Mac when using port to install the docbook-xml and docbook-xsl packages
    # alternatively, docbook is in the dependency of dia,
    /opt/local/share/xsl/docbook-xsl/html
    ${DOCBOOK_HTML_XSL_DIRECTORY}
    )
  set(DOCBOOK_HTML_XSL ${DOCBOOK_HTML_XSL_DIRECTORY}/docbook.xsl)
  set(DOCBOOK_HTML_CHUNK_XSL ${DOCBOOK_HTML_XSL_DIRECTORY}/chunk.xsl)
  set(DOCBOOK_HTML_CHUNKFAST_XSL ${DOCBOOK_HTML_XSL_DIRECTORY}/chunkfast.xsl)
  get_filename_component(
    DOCBOOK_XSL_DIRECTORY
    ${DOCBOOK_HTML_XSL_DIRECTORY}/..
    ABSOLUTE
    )

  if(DOCBOOK_USE_SYNTAX_HIGHLIGHTING)
    set(DOCBOOK_HIGHLIGHT_HTML_XSL ${DOCBOOK_HTML_XSL_DIRECTORY}/highlight.xsl)
    set(DOCBOOK_IMPORT_HTML_SYNTAX_HIGHLIGHTING "<xsl:import href=\"${DOCBOOK_HIGHLIGHT_HTML_XSL}\"/>")
  endif(DOCBOOK_USE_SYNTAX_HIGHLIGHTING)
  mark_as_advanced(
    XSLTPROC_EXECUTABLE
    DOCBOOK_HTML_XSL_DIRECTORY
  )
  find_package_handle_standard_args(DocBook
    "DocBook/HTML could not be found"
    XSLTPROC_EXECUTABLE
    DOCBOOK_HTML_XSL_DIRECTORY
    )
endif(DOCBOOK_BUILD_HTML)

#if(DOCBOOK_BUILD_XHTML)
#  find_program(XSLTPROC_EXECUTABLE xsltproc)
#  find_path(DOCBOOK_XHTML_XSL_DIRECTORY docbook.xsl
#    /usr/share/xml/docbook/stylesheet/docbook-xsl/xhtml/
#    #
#    /usr/share/xml/docbook/stylesheet/nwalsh/xhtml/
#    )
#  set(DOCBOOK_XHTML_XSL ${DOCBOOK_XHTML_XSL_DIRECTORY}/docbook.xsl)
#  set(DOCBOOK_XHTML_CHUNK_XSL ${DOCBOOK_XHTML_XSL_DIRECTORY}/chunk.xsl)
#  set(DOCBOOK_XHTML_CHUNKFAST_XSL ${DOCBOOK_XHTML_XSL_DIRECTORY}/chunkfast.xsl)
#  mark_as_advanced(
#    XSLTPROC_EXECUTABLE
#    DOCBOOK_XHTML_XSL_DIRECTORY
#  )
#  find_package_handle_standard_args(DocBook
#    "DocBook/XHTML could not be found"
#    XSLTPROC_EXECUTABLE
#    DOCBOOK_XHTML_XSL_DIRECTORY
#    )
#endif(DOCBOOK_BUILD_XHTML)

if(DOCBOOK_BUILD_PDF)
  find_program(XSLTPROC_EXECUTABLE xsltproc)
  # apt-get install fop
  find_program(FOP_EXECUTABLE fop)
  find_path(DOCBOOK_FO_XSL_DIRECTORY docbook.xsl
    /usr/share/xml/docbook/stylesheet/docbook-xsl/fo/
    /usr/share/sgml/docbook/xsl-stylesheets-1.75.2/fo/
    # older ubuntu:
    /usr/share/xml/docbook/stylesheet/nwalsh/fo/
    # mac when installed with port
    /opt/local/share/xsl/docbook-xsl/fo
    )
  set(DOCBOOK_FO_XSL ${DOCBOOK_FO_XSL_DIRECTORY}/docbook.xsl)
  if(NOT DOCBOOK_XSL_DIRECTORY)
    get_filename_component(
      DOCBOOK_XSL_DIRECTORY
      ${DOCBOOK_FO_XSL_DIRECTORY}/..
      ABSOLUTE
      )
  endif(NOT DOCBOOK_XSL_DIRECTORY)
  if(DOCBOOK_USE_SYNTAX_HIGHLIGHTING)
    set(DOCBOOK_HIGHLIGHT_FO_XSL ${DOCBOOK_FO_XSL_DIRECTORY}/highlight.xsl)
    set(DOCBOOK_IMPORT_FO_SYNTAX_HIGHLIGHTING "<xsl:import href=\"${DOCBOOK_HIGHLIGHT_FO_XSL}\"/>")
  endif(DOCBOOK_USE_SYNTAX_HIGHLIGHTING)
  mark_as_advanced(
    DOCBOOK_FO_XSL_DIRECTORY
    FOP_EXECUTABLE
    XSLTPROC_EXECUTABLE
  )
  option(DOCBOOK_OPTIMIZE_PDF "Optimize PDF file?" OFF)
  mark_as_advanced(DOCBOOK_OPTIMIZE_PDF)
  if(DOCBOOK_OPTIMIZE_PDF)
    # apt-get install ghostscript
    find_program(PDFOPT_EXECUTABLE pdfopt)
    mark_as_advanced(PDFOPT_EXECUTABLE)
    find_package_handle_standard_args(DocBook
      "DocBook/pdfopt could not be found"
      PDFOPT_EXECUTABLE
      )
  endif(DOCBOOK_OPTIMIZE_PDF)
  find_package_handle_standard_args(DocBook
    "DocBook/PDF could not be found"
    DOCBOOK_FO_XSL_DIRECTORY
    FOP_EXECUTABLE
    XSLTPROC_EXECUTABLE
    )
  if(DOCBOOK_USE_SAXON)
    find_program(SAXON_XSLT_EXECUTABLE saxon-xslt)
    mark_as_advanced(
      SAXON_XSLT_EXECUTABLE
      )
  endif(DOCBOOK_USE_SAXON)
endif(DOCBOOK_BUILD_PDF)

#if(DOCBOOK_BUILD_VALIDATION)
  # need xmllint: LIBXML2_XMLLINT_EXECUTABLE in all cases since it generates the full trace (XIncluded files)
  find_package(LibXml2 REQUIRED)
#endif(DOCBOOK_BUILD_VALIDATION)

if(DOCBOOK_BUILD_SPELLCHECK)
  #find_package(ASPELL REQUIRED) # only search for lib/include
  # apt-get install aspell aspell-en
  find_program(ASPELL_EXECUTABLE aspell)
  mark_as_advanced(
    ASPELL_EXECUTABLE
    )
  find_package_handle_standard_args(DocBook
    "DocBook/aspell could not be found"
    ASPELL_EXECUTABLE
    )
endif(DOCBOOK_BUILD_SPELLCHECK)

# Do the dia part:
if(WIN32)
  find_program(DIA_EXECUTABLE dia PATHS "C:/Program Files (x86)/Dia/Bin" "C:/Program Files/Dia/Bin")
else()
  find_program(DIA_EXECUTABLE dia)
endif()
mark_as_advanced(
  DIA_EXECUTABLE
  )
find_package_handle_standard_args(DocBook
  "DocBook/dia could not be found"
  DIA_EXECUTABLE
  )

set(DocBook_USE_FILE ${DocBook_CURRENT_LIST_DIR}/UseDocBook.cmake)


