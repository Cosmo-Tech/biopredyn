configure_file(
  ${CMAKE_CURRENT_SOURCE_DIR}/CustomizationLayer/html/PrototypeGuide.xsl.in
  ${CMAKE_CURRENT_BINARY_DIR}/CustomizationLayer/html/PrototypeGuide.xsl
  @ONLY
)
configure_file(
  ${CMAKE_CURRENT_SOURCE_DIR}/CustomizationLayer/fo/PrototypeGuide.xsl.in
  ${CMAKE_CURRENT_BINARY_DIR}/CustomizationLayer/fo/PrototypeGuide.xsl
  @ONLY
)

set_source_files_properties(
  PrototypeUserGuide.xml
  PROPERTIES DOCBOOK_CUSTOM_HTML ${CMAKE_CURRENT_BINARY_DIR}/CustomizationLayer/html/PrototypeGuide.xsl
)
set_source_files_properties(
  PrototypeUserGuide.xml
  PROPERTIES DOCBOOK_CUSTOM_FO   ${CMAKE_CURRENT_BINARY_DIR}/CustomizationLayer/fo/PrototypeGuide.xsl
)
set_source_files_properties(
  PrototypeUserGuide.xml
  PROPERTIES DOCBOOK_DESTINATION share/doc/Prototype
)

set_source_files_properties(
  TrainingGuide.xml
  PROPERTIES DOCBOOK_CUSTOM_HTML ${CMAKE_CURRENT_BINARY_DIR}/CustomizationLayer/html/PrototypeGuide.xsl
)
set_source_files_properties(
  TrainingGuide.xml
  PROPERTIES DOCBOOK_CUSTOM_FO   ${CMAKE_CURRENT_BINARY_DIR}/CustomizationLayer/fo/PrototypeGuide.xsl
)
set_source_files_properties(
  TrainingGuide.xml
  PROPERTIES DOCBOOK_DESTINATION share/doc/Prototype
)

add_docbook(
  PrototypeUserGuide.xml
)
add_docbook(
  TrainingGuide.xml
)