set(TEST_PY_IN ${CMAKE_CURRENT_SOURCE_DIR}/test.py.in)
set(TEST_PY ${CMAKE_CURRENT_BINARY_DIR}/test.py)

configure_file(${TEST_PY_IN} ${TEST_PY})

macro(bpdAddTest test_name class)
  add_test(
          NAME ${test_name} 
          WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR} 
          COMMAND ${PYTHON_EXECUTABLE} ${TEST_PY} ${class})
  set_tests_properties(${test_name} PROPERTIES DEPENDS BioPreDynPackageInstall)
endmacro()

# Package needs to be installed first
add_test(
  bpdInstallPackage
  ${CMAKE_COMMAND} -P ${CMAKE_BINARY_DIR}/cmake_install.cmake
)

# SBML related tests
bpdAddTest(bpdSBMLLocalImportTest SBMLTestCase.test_local_import)
bpdAddTest(bpdSBMLServerImportTest SBMLTestCase.test_server_import)
bpdAddTest(bpdSBMLBioModelsImportTest SBMLTestCase.test_biomodels_import)
bpdAddTest(bpdSBMLWriteModelTest SBMLTestCase.test_write_model)

# SEDML related tests
bpdAddTest(bpdSEDMLCopasiTimeCourseTest SEDMLTestCase.test_copasi_time_course)
bpdAddTest(bpdSEDMLLibSBMLSimTimeCourseTest SEDMLTestCase.test_libsbmlsim_time_course)

# Output related tests
bpdAddTest(bpdOutputGraphicalOutputTest OutputTestCase.test_graphical_output)
bpdAddTest(bpdOutput3DGraphicalOutputTest OutputTestCase.test_3D_graphical_output)
bpdAddTest(bpdOutputCSVReportTest OutputTestCase.test_csv_report)
bpdAddTest(bpdOutputNUMLReportTest OutputTestCase.test_numl_report)

# Result related tests
bpdAddTest(bpdResultCSVImportTest ResultTestCase.test_csv_import)
bpdAddTest(bpdResultNUMLImportTest ResultTestCase.test_numl_import)
bpdAddTest(bpdTimeSeriesCSVImportTest ResultTestCase.test_csv_import_time_series)
bpdAddTest(bpdTimeSeriesNUMLImportTest ResultTestCase.test_numl_import_time_series)

# XPath related tests
bpdAddTest(bpdXPathUnresolvedXPathTest XPathTestCase.test_unresolved_xpath)
bpdAddTest(bpdXPathReadValueTest XPathTestCase.test_read_value)
bpdAddTest(bpdXPathReturnNodeListTest XPathTestCase.test_return_node_list)

# Change related tests
bpdAddTest(bpdChangeAttributeValueTest ChangeTestCase.test_attribute_value)
bpdAddTest(bpdChangeComputeValueTest ChangeTestCase.test_compute_value)
bpdAddTest(bpdChangeRemoveXMLTest ChangeTestCase.test_remove_xml)
bpdAddTest(bpdChangeAddXMLTest ChangeTestCase.test_add_xml)
bpdAddTest(bpdChangeChangeXMLTest ChangeTestCase.test_change_xml)

# RepeatedTask related tests
bpdAddTest(bpdRepeatedTaskUniformRangeTest RepeatedTaskTestCase.test_uniform_range)
bpdAddTest(bpdRepeatedTaskVectorRangeTest RepeatedTaskTestCase.test_vector_range)
bpdAddTest(
  bpdRepeatedTaskFunctionalRangeTest RepeatedTaskTestCase.test_functional_range)

# OneStep related tests
bpdAddTest(bpdOneStep OneStepTestCase.test_one_step)

# SteadyState related tests
bpdAddTest(bpdSteadyStateCobrapyFBA SteadyStateTestCase.test_fba_cobrapy)
bpdAddTest(bpdSteadyStateLibFbcFBA SteadyStateTestCase.test_fba_libfbc)

# Data generation related tests
bpdAddTest(bpdHomoscedasticDataGenCSV DataGenerationTestCase.test_homoscedastic_csv)
bpdAddTest(
  bpdHeteroscedasticDataGenCSV DataGenerationTestCase.test_heteroscedastic_csv)
bpdAddTest(
  bpdHomoscedasticDataGenNuML DataGenerationTestCase.test_homoscedastic_numl)
bpdAddTest(
  bpdHeteroscedasticDataGenNuML DataGenerationTestCase.test_heteroscedastic_numl)
