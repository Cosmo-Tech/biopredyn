configure_file(
  ${CMAKE_CURRENT_SOURCE_DIR}/CustomizationLayer/html/IntegratedSoftwareSuiteGuide.xsl.in
  ${CMAKE_CURRENT_BINARY_DIR}/CustomizationLayer/html/IntegratedSoftwareSuiteGuide.xsl
  @ONLY
)
configure_file(
  ${CMAKE_CURRENT_SOURCE_DIR}/CustomizationLayer/fo/IntegratedSoftwareSuiteGuide.xsl.in
  ${CMAKE_CURRENT_BINARY_DIR}/CustomizationLayer/fo/IntegratedSoftwareSuiteGuide.xsl
  @ONLY
)

set_source_files_properties(
  IntegratedSoftwareSuiteRequirementsGuide.xml
  PROPERTIES DOCBOOK_CUSTOM_HTML ${CMAKE_CURRENT_BINARY_DIR}/CustomizationLayer/html/IntegratedSoftwareSuiteGuide.xsl
)
set_source_files_properties(
  IntegratedSoftwareSuiteRequirementsGuide.xml
  PROPERTIES DOCBOOK_CUSTOM_FO   ${CMAKE_CURRENT_BINARY_DIR}/CustomizationLayer/fo/IntegratedSoftwareSuiteGuide.xsl
)
set_source_files_properties(
  IntegratedSoftwareSuiteRequirementsGuide.xml
  PROPERTIES DOCBOOK_DESTINATION share/doc/IntegratedSoftwareSuite
)

set_source_files_properties(
  GraphicalUserInterfaceRequirementsGuide.xml
  PROPERTIES DOCBOOK_CUSTOM_HTML ${CMAKE_CURRENT_BINARY_DIR}/CustomizationLayer/html/IntegratedSoftwareSuiteGuide.xsl
)
set_source_files_properties(
  GraphicalUserInterfaceRequirementsGuide.xml
  PROPERTIES DOCBOOK_CUSTOM_FO   ${CMAKE_CURRENT_BINARY_DIR}/CustomizationLayer/fo/IntegratedSoftwareSuiteGuide.xsl
)
set_source_files_properties(
  GraphicalUserInterfaceRequirementsGuide.xml
  PROPERTIES DOCBOOK_DESTINATION share/doc/IntegratedSoftwareSuite
)

add_docbook(
  IntegratedSoftwareSuiteRequirementsGuide.xml
)

add_docbook(
  GraphicalUserInterfaceRequirementsGuide.xml
)