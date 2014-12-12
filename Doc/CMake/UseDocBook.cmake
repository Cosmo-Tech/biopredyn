# Use file for DocBook cmake module (currently only docbook up to version 4.5 is supported)
# This module defines 3 macros:
# add_docbook ( input.xml )
#     - Macro to generate an output document (HTML, PDF, ...) from an input dia docbook file
# dia2png     ( input.dia )
#     - Macro to generate a png file from an input dia file
# dia2svg     ( input.dia )
#     - Macro to generate a svg file from an input dia file
# generate_docbook_sitemap()
#     - Macro to generate the sitemap file. This is a required step for generating olinks
#
# It defines the following variables:
# HTML:
# - DOCBOOK_HTML_XSL_DIRECTORY: Path where to find the html/docbook.xsl XSLT file
# - DOCBOOK_HTML_CHUNKFAST_XSL: Path to the html/chunkfast.xsl XSLT file
# - DOCBOOK_HTML_CHUNK_XSL    : Path to the html/chunk.xsl XSLT file
# - DOCBOOK_HTML_XSL          : Path to the html/docbook.xsl XSLT file
# FO/PDF:
# - DOCBOOK_FO_XSL_DIRECTORY  : Path where to find the fo/docbook.xsl XSLT file
# - DOCBOOK_FO_XSL            : Path to the fo/docbook.xsl XSLT file
#
# The following property are read from the input file:
# - DOCBOOK_CUSTOM_HTML       : Path to specify a particular customization layer for HTML
# - DOCBOOK_CUSTOM_FO         : Path to specify a particular customization layer for FO

# The following global properly will contains the list of all harvested olink
# individual target name
set_property(GLOBAL PROPERTY OLINKDB_HTML_TARGET_NAMES "")
set_property(GLOBAL PROPERTY OLINKDB_PDF_TARGET_NAMES "")
# The following file contains the flat structure of file to be installed. This
# is required when generating olink targetset XML file
file(WRITE "${CMAKE_BINARY_DIR}/docbook_html_sitemap" "")
file(WRITE "${CMAKE_BINARY_DIR}/docbook_pdf_sitemap" "")

# Add a variable for diaconvert that serves as identifier when having duplicate file name.
# Don't use the file path because it may be too long
set(diaconvert_id 0 CACHE INTERNAL "dia convert identifier" FORCE)

macro(checksum_path output path)
  string(REPLACE "/" "_" path_val ${path})

  if(NOT DEFINED ${path_val})
    math(EXPR diaconvert_id "${diaconvert_id} + 1")
    set(diaconvert_id ${diaconvert_id} CACHE INTERNAL "dia convert identifier" FORCE)
    set(${path_val} ${diaconvert_id} CACHE INTERNAL "path ${path_val}" FORCE)
  endif()

  set(${output} ${${path_val}})
endmacro()

macro(compute_project_path output path_we format)
  # compute the path's checksum
  checksum_path(path_id ${path_we})

  # get a subpart of the name to not have too long names
  get_filename_component(path_name_only ${path_we} NAME_WE)
  string(LENGTH ${path_name_only} name_length)
  if(${name_length} LESS 30)
    set(final_name ${path_name_only})
  else()
    math(EXPR name_start "${name_length} - 30")
    string(SUBSTRING ${path_name_only} ${name_start} 30 final_name)
  endif()

  set(${output} dia_${format}_${path_id}_${final_name})
endmacro()

macro(add_docbook input_xml)
  # construct full path to XML file:
  set(input_file)
  if(EXISTS ${input_xml})
    set(input_file ${input_xml})
  else()
    if(EXISTS ${CMAKE_CURRENT_SOURCE_DIR}/${input_xml})
      set(input_file ${CMAKE_CURRENT_SOURCE_DIR}/${input_xml})
    else()
      message(FATAL_ERROR "Non existing file: ${input_xml}")
    endif()
  endif()

  get_filename_component(name_only
    ${input_file}
    NAME_WE)

  #add_custom_target(${name_only}_deps ALL
  #  COMMAND xmllint --xinclude --noout --load-trace ${input_file}
  #  DEPENDS ${input_file}
  #  COMMENT "Generating deps from: ${input_file}"
  #  )
  # In order to track dependencie one need to check the output of:
  #$ xmllint --xinclude --noout --load-trace input.xml
  execute_process(
    COMMAND ${LIBXML2_XMLLINT_EXECUTABLE} --catalogs --xinclude --noout --load-trace ${input_file}
    ERROR_VARIABLE variable
    ERROR_STRIP_TRAILING_WHITESPACE)
  string(REGEX REPLACE "\r?\n" ";" variable "${variable}")
  foreach(file ${variable})
    string(REGEX MATCH "^Loaded URL=\"(.*)\" ID=\"[(]null[)]\"$" nfiletest "${file}")
    # We need to dicard those:
    # Loaded URL=".../docbookV4.5/docbookx.dtd" ID="-//OASIS//DTD DocBook XML V4.5//EN"
    if(nfiletest)
      string(REGEX REPLACE "^Loaded URL=\"(.*)\" ID=\"[(]null[)]\"$" "\\1" nfile "${file}")
      #message("Found: ${nfile} for ${input_file}")
      set(${name_only}_dep_list ${${name_only}_dep_list} ${nfile})
    endif()

    # in case of XML not yes generated we have to parse a warning:
    string(REGEX MATCH "^warning: failed to load external entity \"(.*)\"$" nfiletest2 "${file}")
    if(nfiletest2)
      string(REGEX REPLACE "^warning: failed to load external entity \"(.*)\"$" "\\1" nfile2 "${file}")
      set(${name_only}_dep_list ${${name_only}_dep_list} ${nfile2})
    endif()
  endforeach()

  # At this point ${${name_only}_dep_list} contains the list of loaded files (XML xi:include)
  # This list contains the input file(as first file).

  # Now that we have tracked th XInclude'd file, do the same for the fileref (SVG, PNG ...)
  # http://www.sagehill.net/docbookxsl/GraphicsLocations.html
  # http://docbook.svn.sourceforge.net/viewvc/docbook/trunk/contrib/xsl/xmldepend/
  # Warning we used a modified xmldepend.xsl file. We removed the XML xi:included from the output
  # since we use an alternate process. We also have a modified copy of xmldepend.xsl file in order
  # to generate a flatten tree of image (for HTML output).
  execute_process(
    COMMAND ${XSLTPROC_EXECUTABLE} ${DocBook_CURRENT_LIST_DIR}/xmldepend.xsl ${input_file}
    OUTPUT_VARIABLE variable
    OUTPUT_STRIP_TRAILING_WHITESPACE)
  string(REGEX REPLACE "\r?\n" ";" img_list "${variable}")

  get_source_file_property(docbook_destination ${input_file} DOCBOOK_DESTINATION)
  set(image_deps) # list of input file(screenshot.png)
  set(image_deps_generated) # list of generate png/svg file(from dia)
  foreach(img ${img_list})
    # Our modified version of xmldepend.xsl will add an extra ',' char in order
    # to distinguish in between generated file from input source file.
    string(REGEX REPLACE "^(.*),.*$" "\\1" file1 "${img}")
    string(REGEX REPLACE "^.*,(.*)$" "\\1" file2 "${img}")
    set(fullpath)
    if(file1)
      set(fullpath ${file1}/${file2})
      set(targetpath ${file2})
    else()
      set(fullpath ${file2})
      set(targetpath ${file2})
    endif()

    # This is the complex part. Since HTML documentation is being flatten A/B/C.xml becomes output/mangled_name.html
    # we need to properly re-copy any required file to the proper path. Do it depending on whether we are generating
    # image file or real input png file:
    if(EXISTS ${CMAKE_CURRENT_SOURCE_DIR}/${fullpath})
      # We need to copy file from source to bin when building HTML or PDF
      add_custom_command(
        OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/${name_only}/${targetpath}
        COMMAND ${CMAKE_COMMAND} -E copy_if_different ${CMAKE_CURRENT_SOURCE_DIR}/${fullpath}
          ${CMAKE_CURRENT_BINARY_DIR}/${name_only}/${targetpath}
        DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/${fullpath})
      if(DOCBOOK_BUILD_HTML)
        # Install those files if requested:
        if(docbook_destination)
          get_filename_component(targetrealpath
            ${CMAKE_CURRENT_BINARY_DIR}/${name_only}/${targetpath}
            REALPATH)
          get_filename_component(targetrealpath_path
            ${targetrealpath}
            PATH)
          string(REPLACE "${CMAKE_CURRENT_BINARY_DIR}/" "" outpath "${targetrealpath_path}")
          install(FILES ${CMAKE_CURRENT_BINARY_DIR}/${name_only}/${targetpath}
            DESTINATION ${docbook_destination}/${outpath})
        endif()
      endif()
      list(APPEND image_deps ${CMAKE_CURRENT_SOURCE_DIR}/${fullpath}
        ${CMAKE_CURRENT_BINARY_DIR}/${name_only}/${targetpath})
    else()
      # Here come the nasty part. We have found a svg/png that will be generated from a dia file.
      # In order for cmake to work across directory level, we cannot simply state that docbook.xml
      # depends on bin/full/path/image.png, since add_custom_command does not work across directories
      # the only work around is to recompute the target name associated to this file by the diaconvert macro
      # Let's do this reverse engineering here:
      get_filename_component(absolute "${CMAKE_CURRENT_BINARY_DIR}/${fullpath}" ABSOLUTE)
      string(REPLACE "${PROJECT_BINARY_DIR}" "" output "${absolute}")

      get_filename_component(target_name_end_tmp "${output}" EXT)
      string(REPLACE "." "" target_name_end "${target_name_end_tmp}")

      get_filename_component(output_path ${output} PATH)
      get_filename_component(output_we ${output} NAME_WE)
      compute_project_path(output_name ${output_path}/${output_we} ${target_name_end})

      # We have found the exact same target name as what would diaconvert would generated, add it to the list:
      list(APPEND image_deps_generated ${output_name})

      # The above line create dependencies in between targets. However this is not enough
      # we still need to say we depend to specific file(this is how cmake works).
      list(APPEND image_deps ${CMAKE_CURRENT_BINARY_DIR}/${fullpath})
      if(DOCBOOK_BUILD_HTML)
        add_custom_command(
          OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/${name_only}/${targetpath}
          COMMAND ${CMAKE_COMMAND} -E copy_if_different ${CMAKE_CURRENT_BINARY_DIR}/${fullpath}
            ${CMAKE_CURRENT_BINARY_DIR}/${name_only}/${targetpath}
          DEPENDS ${CMAKE_CURRENT_BINARY_DIR}/${fullpath})
        list(APPEND image_deps ${CMAKE_CURRENT_BINARY_DIR}/${name_only}/${targetpath})
        # Install those files if requested:
        if(docbook_destination)
          get_filename_component(targetrealpath
            ${CMAKE_CURRENT_BINARY_DIR}/${name_only}/${targetpath}
            REALPATH)
          get_filename_component(targetrealpath_path
            ${targetrealpath}
            PATH)
          string(REPLACE "${CMAKE_CURRENT_BINARY_DIR}/" "" outpath "${targetrealpath_path}")
          install(FILES ${CMAKE_CURRENT_BINARY_DIR}/${name_only}/${targetpath}
            DESTINATION ${docbook_destination}/${outpath})
        endif()
      endif()
    endif()
  endforeach()

  # Do the XInclude since saxon does not support it.
  add_custom_command(
    OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/${name_only}.xinclude.xml
    COMMAND ${LIBXML2_XMLLINT_EXECUTABLE} --catalogs --postvalid --xinclude
      --output ${CMAKE_CURRENT_BINARY_DIR}/${name_only}.xinclude.xml ${input_file}
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    DEPENDS ${input_file} ${${name_only}_dep_list} ${image_deps})
  # http://www.sagehill.net/docbookxsl/Olinking.html
  # -> 5. Generate target data files
  # HTML
  if(DOCBOOK_BUILD_HTML)
    add_custom_command(
      OUTPUT ${CMAKE_BINARY_DIR}/${name_only}.olinkdb.html.xml
      COMMAND ${XSLTPROC_EXECUTABLE} --catalogs --xinclude --stringparam collect.xref.targets only
        --stringparam olink.base.uri "/" --stringparam targets.filename
        "${CMAKE_BINARY_DIR}/${name_only}.olinkdb.html.xml" ${DOCBOOK_HTML_CHUNKFAST_XSL} ${input_file}
      DEPENDS ${input_file} ${${name_only}_dep_list})
    add_custom_target(
      ${name_only}_olinkdb_html
      DEPENDS ${CMAKE_BINARY_DIR}/${name_only}.olinkdb.html.xml)
    get_property(olinkdb_html_target_names GLOBAL PROPERTY OLINKDB_HTML_TARGET_NAMES)
    list(APPEND olinkdb_html_target_names "${name_only}_olinkdb_html")
    set_property(GLOBAL PROPERTY OLINKDB_HTML_TARGET_NAMES ${olinkdb_html_target_names})
  endif()
  # PDF
  if(DOCBOOK_BUILD_PDF)
    add_custom_command(
      OUTPUT ${CMAKE_BINARY_DIR}/${name_only}.olinkdb.pdf.xml
      COMMAND ${XSLTPROC_EXECUTABLE} --catalogs --xinclude --stringparam collect.xref.targets only
      --stringparam targets.filename "${CMAKE_BINARY_DIR}/${name_only}.olinkdb.pdf.xml"
      ${DOCBOOK_FO_XSL} ${input_file}
      DEPENDS ${input_file} ${${name_only}_dep_list})
    add_custom_target(
      ${name_only}_olinkdb_pdf
      DEPENDS ${CMAKE_BINARY_DIR}/${name_only}.olinkdb.pdf.xml)
    get_property(olinkdb_pdf_target_names GLOBAL PROPERTY OLINKDB_PDF_TARGET_NAMES)
    list(APPEND olinkdb_pdf_target_names "${name_only}_olinkdb_pdf")
    set_property(GLOBAL PROPERTY OLINKDB_PDF_TARGET_NAMES ${olinkdb_pdf_target_names})
  endif()

  # xmlto --skip-validation html article.xml
  if(DOCBOOK_BUILD_HTML)
    # We are outputting all HTML files within this directory:
    file(MAKE_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/${name_only})
    set(current_docbook_html_xsl ${DOCBOOK_HTML_CHUNKFAST_XSL})
    get_source_file_property(custom_html ${input_file} DOCBOOK_CUSTOM_HTML)
    # User requested a particuler XSL customization layer. let's use it
    if(custom_html)
      if(EXISTS ${custom_html})
        set(current_docbook_html_xsl ${custom_html})
      else()
        if(EXISTS ${CMAKE_CURRENT_SOURCE_DIR}/${custom_html})
          set(current_docbook_html_xsl ${CMAKE_CURRENT_SOURCE_DIR}/${custom_html})
        else()
          message(FATAL_ERROR "Non existing file: ${custom_html}")
        endif()
      endif()
    endif()
    #add_custom_command(
    #  OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/${name_only}/index.html
    #  COMMAND ${XMLTO_EXECUTABLE} --skip-validation html -o ${CMAKE_CURRENT_BINARY_DIR}/${name_only} ${input_file}
    #  DEPENDS ${input_file} ${${name_only}_dep_list}
    #  )
    # Avoid using xmlto which is not configurable
    # http://www.sagehill.net/docbookxsl/Chunking.html#base.dirParam
    if(DOCBOOK_USE_SAXON)
      set(resolverPath ${XML_COMMONS_RESOLVER_CATALOGMANAGER_PROPERTIES_PATH})
      add_custom_command(
        OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/${name_only}/index.html
        COMMAND ${JAVA_RUNTIME}
          -cp ${resolverPath}:${XSLTHL_JAR}:${XML_COMMONS_RESOLVER_JAR}:${DOCBOOK_XSL_SAXON_JAR}:${SAXON_JAR}
          com.icl.saxon.StyleSheet
          -x org.apache.xml.resolver.tools.ResolvingXMLReader
          -y org.apache.xml.resolver.tools.ResolvingXMLReader
          -r org.apache.xml.resolver.tools.CatalogResolver
          -u ${CMAKE_CURRENT_BINARY_DIR}/${name_only}.xinclude.xml
          ${current_docbook_html_xsl}
          use.extensions=1
          keep.relative.image.uris=1
          base.dir=${CMAKE_CURRENT_BINARY_DIR}/${name_only}/
          target.database.document=${CMAKE_BINARY_DIR}/olinkdb.html.xml
        # we do not need to add dep to ${image_deps} in HTML output
        WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/${name_only}
        DEPENDS ${current_docbook_html_xsl} ${CMAKE_CURRENT_BINARY_DIR}/${name_only}.xinclude.xml)
    else()
      add_custom_command(
        OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/${name_only}/index.html
        COMMAND ${XSLTPROC_EXECUTABLE}
        --catalogs
        --stringparam keep.relative.image.uris 1
        # img.src.path is a bad idea since it would couple src and output. we want to be able to export the
        # documentation without distributing the source. We also want to be able to generate png from say .dia file...
        #--stringparam img.src.path ${CMAKE_CURRENT_SOURCE_DIR}
        # http://docbook.sourceforge.net/release/xsl/current/doc/html/index.html
        #--stringparam ulink.target bla
        --stringparam base.dir ${CMAKE_CURRENT_BINARY_DIR}/${name_only}/
        --stringparam target.database.document ${CMAKE_BINARY_DIR}/olinkdb.html.xml
        ${current_docbook_html_xsl} ${CMAKE_CURRENT_BINARY_DIR}/${name_only}.xinclude.xml
        #WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
        # we do not need to add dep to ${image_deps} in HTML output
        DEPENDS ${current_docbook_html_xsl} ${CMAKE_CURRENT_BINARY_DIR}/${name_only}.xinclude.xml)
    endif()
    if(docbook_destination)
      install(DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/${name_only}
        DESTINATION ${docbook_destination})
      file(APPEND "${CMAKE_BINARY_DIR}/docbook_html_sitemap"
        "<file><path>${docbook_destination}/${name_only}/index.html</path></file>")
    endif()

    # need to give unique name to target:
    add_custom_target(${name_only}_html ALL
      DEPENDS ${CMAKE_CURRENT_BINARY_DIR}/${name_only}/index.html
      COMMENT "Generating HTML from: ${input_file} into ${CMAKE_CURRENT_BINARY_DIR}/${name_only}/index.html")
    # We need to make sure that olinks.html.xml is present in case document need to olink to external doc.
    add_dependencies(${name_only}_html
      docbook_olinkdb_html_generate)
    foreach(generated ${image_deps_generated})
      add_dependencies(${name_only}_html ${generated})
    endforeach()
  endif()

  # xsltproc --xinclude -o article.fo /usr/share/xml/docbook/stylesheet/docbook-xsl/fo/docbook.xsl article.xml
  # fop -fo article.fo -pdf article.pdf
  # http://www.sagehill.net/docbookxsl/InstallingAnFO.html#UsingFop
  if(DOCBOOK_BUILD_PDF)
    set(current_docbook_fo_xsl ${DOCBOOK_FO_XSL})
    get_source_file_property(custom_fo ${input_file} DOCBOOK_CUSTOM_FO)
    # User requested a particuler XSL customization layer. let's use it
    if(custom_fo)
      if(EXISTS ${custom_fo})
        set(current_docbook_fo_xsl ${custom_fo})
      else()
        if(EXISTS ${CMAKE_CURRENT_SOURCE_DIR}/${custom_fo})
          set(current_docbook_fo_xsl ${CMAKE_CURRENT_SOURCE_DIR}/${custom_fo})
        else()
          message(FATAL_ERROR "Non existing file: ${custom_fo}")
        endif()
      endif()
    endif()

    if(DOCBOOK_OPTIMIZE_PDF)
      set(output_pdf_filename ${CMAKE_CURRENT_BINARY_DIR}/${name_only}.tmp.pdf)
    else()
      set(output_pdf_filename ${CMAKE_CURRENT_BINARY_DIR}/${name_only}.pdf)
    endif()
    if(DOCBOOK_USE_SAXON)
      set(resolverPath ${XML_COMMONS_RESOLVER_CATALOGMANAGER_PROPERTIES_PATH})
      add_custom_command(
        OUTPUT ${output_pdf_filename}
        COMMAND ${JAVA_RUNTIME}
          -cp ${resolverPath}:${XSLTHL_JAR}:${XML_COMMONS_RESOLVER_JAR}:${DOCBOOK_XSL_SAXON_JAR}:${SAXON_JAR}
          com.icl.saxon.StyleSheet
          -x org.apache.xml.resolver.tools.ResolvingXMLReader
          -y org.apache.xml.resolver.tools.ResolvingXMLReader
          -r org.apache.xml.resolver.tools.CatalogResolver
          -u
          -o ${CMAKE_CURRENT_BINARY_DIR}/${name_only}.fo
          ${CMAKE_CURRENT_BINARY_DIR}/${name_only}.xinclude.xml
          ${current_docbook_fo_xsl}
          fop1.extensions=1
          use.extensions=1
          target.database.document=${CMAKE_BINARY_DIR}/olinkdb.pdf.xml
        COMMAND ${FOP_EXECUTABLE} -c ${DocBook_CURRENT_LIST_DIR}/fop.xconf
          -fo ${CMAKE_CURRENT_BINARY_DIR}/${name_only}.fo -pdf ${output_pdf_filename}
        # fop seems to require the source directory in order to find relative file, eg: ../my/image.png
        WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
        # need to depends on image
        DEPENDS ${current_docbook_fo_xsl}
          ${CMAKE_CURRENT_BINARY_DIR}/${name_only}.xinclude.xml
          ${DocBook_CURRENT_LIST_DIR}/fop.xconf)
    else()
      add_custom_command(
        OUTPUT ${output_pdf_filename}
        COMMAND ${XSLTPROC_EXECUTABLE}
        --catalogs
        --stringparam use.extensions 1
        --stringparam fop1.extensions 1
        --stringparam tablecolumns.extension 0 # This is not supported by libxslt
        --stringparam callouts.extension 0 # This is not supported by libxslt
        --stringparam target.database.document ${CMAKE_BINARY_DIR}/olinkdb.pdf.xml
        -o ${CMAKE_CURRENT_BINARY_DIR}/${name_only}.fo
        ${current_docbook_fo_xsl}
        ${CMAKE_CURRENT_BINARY_DIR}/${name_only}.xinclude.xml
        COMMAND ${FOP_EXECUTABLE} -c ${DocBook_CURRENT_LIST_DIR}/fop.xconf
          -fo ${CMAKE_CURRENT_BINARY_DIR}/${name_only}.fo -pdf ${output_pdf_filename}
        # fop seems to require the source directory in order to find relative file, eg: ../my/image.png
        WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
        # need to depends on image
        DEPENDS ${current_docbook_fo_xsl}
          ${CMAKE_CURRENT_BINARY_DIR}/${name_only}.xinclude.xml
          ${DocBook_CURRENT_LIST_DIR}/fop.xconf)
    endif()
    if(DOCBOOK_OPTIMIZE_PDF)
      add_custom_command(
        OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/${name_only}.pdf
        COMMAND ${PDFOPT_EXECUTABLE} ${output_pdf_filename} ${CMAKE_CURRENT_BINARY_DIR}/${name_only}.pdf
        DEPENDS ${output_pdf_filename})
    endif()
    #message("${name_only} : ${image_deps}")
    #message("${name_only} : ${${name_only}_dep_list}")
    if(docbook_destination)
      install(FILES ${CMAKE_CURRENT_BINARY_DIR}/${name_only}.pdf
        DESTINATION ${docbook_destination})
      file(APPEND "${CMAKE_BINARY_DIR}/docbook_pdf_sitemap"
        "<file><path>${docbook_destination}/${name_only}.pdf</path></file>")
    endif()

    add_custom_target(${name_only}_pdf ALL
      DEPENDS ${CMAKE_CURRENT_BINARY_DIR}/${name_only}.pdf
      COMMENT "Generating PDF from: ${input_file} into ${CMAKE_CURRENT_BINARY_DIR}/${name_only}.pdf")
    # We need to make sure that olinks.pdf.xml is present in case document need to olink to external doc.
    add_dependencies(${name_only}_pdf
      docbook_olinkdb_pdf_generate)
    foreach(generated ${image_deps_generated})
      add_dependencies(${name_only}_pdf ${generated})
    endforeach()
  endif()

  if(DOCBOOK_BUILD_VALIDATION)
    # add_custom_target:  is ALWAYS CONSIDERED OUT OF DATE
    add_custom_target(${name_only}_validate ALL
      #COMMAND xmllint --xinclude --noent --postvalid --noout --nonet --valid ${CMAKE_CURRENT_SOURCE_DIR}/article.xml
      COMMAND ${LIBXML2_XMLLINT_EXECUTABLE} --catalogs --xinclude --postvalid --noout --nonet ${input_file}
      DEPENDS ${input_file} ${${name_only}_dep_list}
      COMMENT "Validating: ${input_file}")
  endif()

  if(DOCBOOK_BUILD_SPELLCHECK)
    set(SGML_SKIP_LIST
      acronym
      application
      author
      code
      hardware
      filename
      markup
      programlisting
      productname
      screen
      sgmltag)
    set(SPELLCHECK_COMMAND
      ${LIBXML2_XMLLINT_EXECUTABLE} --postvalid --xinclude --nonet ${input_file}
      | ${ASPELL_EXECUTABLE} list -p ${DocBook_CURRENT_LIST_DIR}/aspell.en.pws --mode=sgml --lang=en --encoding=utf-8)
    # As long as we avoid spaces in strings we should be ok:
    foreach(skip ${SGML_SKIP_LIST})
      list(APPEND SPELLCHECK_COMMAND "--add-f-sgml-skip=${skip}")
    endforeach()
    if(UNIX)
      list(APPEND SPELLCHECK_COMMAND "|sort|uniq")
    endif()
    add_custom_target(${name_only}_spellcheck ALL
      COMMAND ${SPELLCHECK_COMMAND}
      COMMAND ${CMAKE_COMMAND} -E echo `${SPELLCHECK_COMMAND} | wc -l` "spell check errors found"
      DEPENDS ${input_file} ${${name_only}_dep_list}
      COMMENT "Spellcheck: ${input_file}")
  endif()

endmacro()

# YES diaconvert needs to be within docbook cmake macro. add_docbook and diaconvert are closely related.
macro(diaconvert output_format input_dia use_filter)
  # construct full path to DIA file:
  set(input_file)
  if(EXISTS ${input_dia})
    set(input_file ${input_dia})
  else()
    if(EXISTS ${CMAKE_CURRENT_SOURCE_DIR}/${input_dia})
      set(input_file ${CMAKE_CURRENT_SOURCE_DIR}/${input_dia})
    else()
      message(FATAL_ERROR "Non existing file: ${input_dia}")
    endif()
  endif()

  get_filename_component(name_only ${input_file} NAME_WE)

  # dia --filter svg --export PlatformTools.svg PlatformTools.dia
  add_custom_command(
    OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/${name_only}.${output_format}
    # http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=538309
    COMMAND ${DIA_EXECUTABLE} -n --filter ${use_filter}
      --export ${CMAKE_CURRENT_BINARY_DIR}/${name_only}.${output_format} ${input_file}
    #WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    DEPENDS ${input_file})
  # Sometime filename conflicts (usually simple redundant file. we need to scope with
  # them and use identifier (path can't be used because it may be too long) to avoid name clash
  string(REPLACE "${PROJECT_SOURCE_DIR}" "" output_path "${CMAKE_CURRENT_SOURCE_DIR}")
  # Path is transformed to a checksum because path can be too long
  compute_project_path(output_name ${output_path}/${name_only} ${output_format})
  #message("conv <<< ${output_path}/${name_only} ${output_format} -> ${output_name}")

  add_custom_target("${output_name}" #ALL
    DEPENDS ${CMAKE_CURRENT_BINARY_DIR}/${name_only}.${output_format})
    #COMMENT "Generating ${output_format} from: ${input_file}"
endmacro()

  # Let's find out which png is supported in dia
  execute_process(
    COMMAND ${DIA_EXECUTABLE} -n --help # -h does not work
    OUTPUT_VARIABLE variable
    ERROR_VARIABLE variable
    OUTPUT_STRIP_TRAILING_WHITESPACE
    ERROR_STRIP_TRAILING_WHITESPACE)

  set(png_filters)
  string(REGEX REPLACE "\r?\n" ";" variable "${variable}")
  foreach(line ${variable})
    string(REGEX MATCH "^.*--filter(.*)$" nfilter "${line}")
    if(nfilter)
      string(REGEX REPLACE "^.*--filter(.*)$" "\\1" nfilter "${line}")
      string(REGEX MATCH "^.*png [(](.*)[)].*$" npng "${nfilter}")
      if(npng)
        string(REGEX REPLACE "^.*png [(](.*)[)].*$" "\\1" npng "${nfilter}")
        string(REGEX REPLACE "," " " png_filters "${npng}")
        separate_arguments(png_filters)
      endif()
    endif()
  endforeach()
  set(png_filter "cairo-alpha-png")
  list(FIND png_filters ${png_filter} cairo_alpha_png_found)
  if(cairo_alpha_png_found GREATER -1)
    #message( "Found !")
  else( )
    # index starts at 0
    list(GET png_filters 0 png_filter)
  endif( )
  # message( "DEBUG dia png filter: ${png_filter}")

macro(dia2png input_dia)
  diaconvert(png ${input_dia} ${png_filter})
endmacro()

macro(dia2svg input_dia)
  diaconvert(svg ${input_dia} svg)
endmacro()

# This macro will convert a doxygen XML generated file into a valid docbook file
macro(add_docbook_example input_xml)
  # DOCBOOK_DOXGEN_XML_DIR specify the path where the doxygen XML file are located
  # typically we can only do that from a build-tree
  if(DOCBOOK_DOXGEN_XML_DIR)
    if(EXISTS ${DOCBOOK_DOXGEN_XML_DIR})
      set(doxygen_xml_dir ${DOCBOOK_DOXGEN_XML_DIR})
    endif()
  endif()
  if(NOT doxygen_xml_dir)
    message(FATAL_ERROR "Could not find DOCBOOK_DOXGEN_XML_DIR: ${DOCBOOK_DOXGEN_XML_DIR}")
  endif()

# Removing mangling since we enabled doxygen short names.
#  set(doxygen_mangling "_8cxx.xml")
  set(doxygen_mangling ".xml")
  set(doxygen_xml_file "${doxygen_xml_dir}/${input_xml}${doxygen_mangling}")
  set(doxygen2docbook_file "${DocBook_CURRENT_LIST_DIR}/doxygen2docbook.xsl")
  if(EXISTS ${doxygen_xml_file})
    add_custom_command(
      OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/${input_xml}.xml
      COMMAND ${XSLTPROC_EXECUTABLE} -o ${CMAKE_CURRENT_BINARY_DIR}/${input_xml}.xml
        ${doxygen2docbook_file} ${doxygen_xml_file}
      DEPENDS ${doxygen_xml_file} ${doxygen2docbook_file})
    add_custom_target(${input_xml}_example ALL
      DEPENDS ${CMAKE_CURRENT_BINARY_DIR}/${input_xml}.xml
      COMMENT "Generating Examples")
  else()
    message(FATAL_ERROR "Could not find doxygen_xml_file: ${doxygen_xml_file}")
  endif()

endmacro()

# This macro should be called only once for all docbook documents that were
# created with add_docbook.
# It will compute the olinkdb.xml file that is necessary to allow linking
# to/from external document
# See also:
#  * http://www.sagehill.net/docbookxsl/Olinking.html
#  * http://www.sagehill.net/docbookxsl/OlinkVariations.html
macro(generate_docbook_sitemap)
  if(DOCBOOK_BUILD_HTML)
  # HTML
  set(outputfile "olinkdb.html.xml")
  # 1. Retrieve the list of olink html individual target
  get_property(olinkdb_html_target_names GLOBAL PROPERTY OLINKDB_HTML_TARGET_NAMES)
  # 2. docbook_html_sitemap contains the list of installation path for each docbook document
  # in a flat structure (as given by cmake)
  file(READ "${CMAKE_BINARY_DIR}/docbook_html_sitemap" GLOBAL_DOCBOOK_LIST)
  configure_file(${DocBook_CURRENT_LIST_DIR}/sitemap.xml.in
    ${CMAKE_BINARY_DIR}/sitemap.html.xml
    @ONLY)
  # 3. convert the flat structure of installation path into a tree-like structure as expected with
  # <!DOCTYPE targetset SYSTEM "file:///docbook-xsl/common/targetdatabase.dtd">
  add_custom_command(
    OUTPUT ${CMAKE_BINARY_DIR}/${outputfile}
    COMMAND ${XSLTPROC_EXECUTABLE} -o ${CMAKE_BINARY_DIR}/sitemap_sorted.html.xml
      ${DocBook_CURRENT_LIST_DIR}/sort.xsl ${CMAKE_BINARY_DIR}/sitemap.html.xml
    COMMAND ${XSLTPROC_EXECUTABLE} -o ${CMAKE_BINARY_DIR}/sitemap_sorted2.html.xml
      ${DocBook_CURRENT_LIST_DIR}/convert_flat_tree_to_targetset_tree.xsl ${CMAKE_BINARY_DIR}/sitemap_sorted.html.xml
    COMMAND ${LIBXML2_XMLLINT_EXECUTABLE} --xinclude --output ${CMAKE_CURRENT_BINARY_DIR}/${outputfile}
      ${CMAKE_BINARY_DIR}/sitemap_sorted2.html.xml
    DEPENDS ${DocBook_CURRENT_LIST_DIR}/sort.xsl ${DocBook_CURRENT_LIST_DIR}/convert_flat_tree_to_targetset_tree.xsl
      ${CMAKE_BINARY_DIR}/sitemap.html.xml)
  # 4. Name this top-level target so that we can add_dependencies to it...
  add_custom_target(docbook_olinkdb_html_generate
    DEPENDS ${CMAKE_BINARY_DIR}/${outputfile}
    COMMENT "Generating Sitemap")
  # 5. Make sure to only build this toplevel olinkdb file when (and only when) individual
  # olinks file have been generated.
  add_dependencies(docbook_olinkdb_html_generate
    ${olinkdb_html_target_names})
  endif()
  # PDF
  if(DOCBOOK_BUILD_PDF)
  set(outputfile "olinkdb.pdf.xml")
  # 1. Retrieve the list of olink pdf individual target
  get_property(olinkdb_pdf_target_names GLOBAL PROPERTY OLINKDB_PDF_TARGET_NAMES)
  # 2. docbook_pdf_sitemap contains the list of installation path for each docbook document
  # in a flat structure (as given by cmake)
  file(READ "${CMAKE_BINARY_DIR}/docbook_pdf_sitemap" GLOBAL_DOCBOOK_LIST)
  configure_file(${DocBook_CURRENT_LIST_DIR}/sitemap.xml.in
    ${CMAKE_BINARY_DIR}/sitemap.pdf.xml
    @ONLY)
  # 3. convert the flat structure of installation path into a tree-like structure as expected with
  # <!DOCTYPE targetset SYSTEM "file:///docbook-xsl/common/targetdatabase.dtd">
  add_custom_command(
    OUTPUT ${CMAKE_BINARY_DIR}/${outputfile}
    COMMAND ${XSLTPROC_EXECUTABLE} -o ${CMAKE_BINARY_DIR}/sitemap_sorted.pdf.xml
      ${DocBook_CURRENT_LIST_DIR}/sort.xsl ${CMAKE_BINARY_DIR}/sitemap.pdf.xml
    COMMAND ${XSLTPROC_EXECUTABLE} -o ${CMAKE_BINARY_DIR}/sitemap_sorted2.pdf.xml
      ${DocBook_CURRENT_LIST_DIR}/convert_flat_tree_to_targetset_tree.xsl ${CMAKE_BINARY_DIR}/sitemap_sorted.pdf.xml
    COMMAND ${LIBXML2_XMLLINT_EXECUTABLE} --xinclude --output ${CMAKE_CURRENT_BINARY_DIR}/${outputfile}
      ${CMAKE_BINARY_DIR}/sitemap_sorted2.pdf.xml
    DEPENDS ${DocBook_CURRENT_LIST_DIR}/sort.xsl ${DocBook_CURRENT_LIST_DIR}/convert_flat_tree_to_targetset_tree.xsl
      ${CMAKE_BINARY_DIR}/sitemap.pdf.xml)
  # 4. Name this top-level target so that we can add_dependencies to it...
  add_custom_target(docbook_olinkdb_pdf_generate
    DEPENDS ${CMAKE_BINARY_DIR}/${outputfile}
    COMMENT "Generating Sitemap")
  # 5. Make sure to only build this toplevel olinkdb file when (and only when) individual
  # olinks file have been generated.
  add_dependencies(docbook_olinkdb_pdf_generate
    ${olinkdb_pdf_target_names})
  endif()
endmacro()

