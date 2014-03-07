set(TEST_PY_IN ${CMAKE_CURRENT_SOURCE_DIR}/test.py.in)
set(TEST_PY ${CMAKE_CURRENT_BINARY_DIR}/test.py)

configure_file(${TEST_PY_IN} ${TEST_PY})

macro(bpdAddTest test_name class)
  add_test(${test_name} ${PYTHON_EXECUTABLE} ${TEST_PY} ${class})
  set_tests_properties(${test_name} PROPERTIES DEPENDS BioPreDynPackageInstall)
endmacro()

# SBML related tests
bpdAddTest(SBMLLocalImportTest SBMLTestCase.test_local_import)
bpdAddTest(SBMLServerImportTest SBMLTestCase.test_server_import)
bpdAddTest(SBMLBioModelsImportTest SBMLTestCase.test_biomodels_import)
bpdAddTest(SBMLWriteModelTest SBMLTestCase.test_write_model)

# SEDML related tests
bpdAddTest(SEDMLLibSBMLSimTimeCourseTest SEDMLTestCase.test_libsbmlsim_time_course)

# Output related tests
bpdAddTest(OutputGraphicalOutputTest OutputTestCase.test_graphical_output)
bpdAddTest(Output3DGraphicalOutputTest OutputTestCase.test_3D_graphical_output)
bpdAddTest(OutputCSVReportTest OutputTestCase.test_csv_report)
bpdAddTest(OutputNUMLReportTest OutputTestCase.test_numl_report)

# Result related tests
bpdAddTest(ResultCSVImportTest ResultTestCase.test_csv_import)
bpdAddTest(ResultNUMLImportTest ResultTestCase.test_numl_import)

# XPath related tests
bpdAddTest(XPathUnresolvedXPathTest XPathTestCase.test_unresolved_xpath)
bpdAddTest(XPathReadValueTest XPathTestCase.test_read_value)
bpdAddTest(XPathReturnNodeListTest XPathTestCase.test_return_node_list)

# Change related tests
bpdAddTest(ChangeAttributeValueTest ChangeTestCase.test_attribute_value)
bpdAddTest(ChangeComputeValueTest ChangeTestCase.test_compute_value)
bpdAddTest(ChangeRemoveXMLTest ChangeTestCase.test_remove_xml)
bpdAddTest(ChangeAddXMLTest ChangeTestCase.test_add_xml)
bpdAddTest(ChangeChangeXMLTest ChangeTestCase.test_change_xml)

# RepeatedTask related tests
bpdAddTest(RepeatedTaskUniformRangeTest RepeatedTaskTestCase.test_uniform_range)