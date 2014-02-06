set(TEST_PY_IN ${CMAKE_CURRENT_SOURCE_DIR}/test.py.in)
set(TEST_PY ${CMAKE_CURRENT_BINARY_DIR}/test.py)
set(SETUP_PY ${CMAKE_BINARY_DIR}/Prototype/python/setup.py)

configure_file(${TEST_PY_IN} ${TEST_PY})

macro(bpdAddTest test_name class)
  add_test(${test_name} ${PYTHON_EXECUTABLE} ${TEST_PY} ${class})
  set_tests_properties(${test_name} PROPERTIES DEPENDS BioPreDynPackageInstall)
endmacro()

# SBML related tests
bpdAddTest(SBMLLocalImportTest SBMLTestCase.test_local_import)
bpdAddTest(SBMLServerImportTest SBMLTestCase.test_server_import)
bpdAddTest(SBMLBioModelsImportTest SBMLTestCase.test_biomodels_import)

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
bpdAddTest(XPathReadValueTest XPathTestCase.test_read_value)
bpdAddTest(XPathReturnNodeListTest XPathTestCase.test_return_node_list)