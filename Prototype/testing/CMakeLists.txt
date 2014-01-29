set(TEST_PY_IN ${CMAKE_CURRENT_SOURCE_DIR}/test.py.in)
set(TEST_PY ${CMAKE_CURRENT_BINARY_DIR}/test.py)

configure_file(${TEST_PY_IN} ${TEST_PY})

# SBML related tests
add_test(SBMLLocalImportTest ${PYTHON_EXECUTABLE}
  ${TEST_PY} SBMLTestCase.test_local_import)
add_test(SBMLServerImportTest ${PYTHON_EXECUTABLE}
  ${TEST_PY} SBMLTestCase.test_server_import)
add_test(SBMLBioModelsImportTest ${PYTHON_EXECUTABLE}
  ${TEST_PY} SBMLTestCase.test_biomodels_import)

# SEDML related tests
add_test(SEDMLLibSBMLSimTimeCourseTest ${PYTHON_EXECUTABLE}
  ${TEST_PY} SEDMLTestCase.test_libsbmlsim_time_course)

# Output related tests
add_test(OutputGraphicalOutputTest ${PYTHON_EXECUTABLE}
  ${TEST_PY} OutputTestCase.test_graphical_output)
add_test(Output3DGraphicalOutputTest ${PYTHON_EXECUTABLE}
  ${TEST_PY} OutputTestCase.test_3D_graphical_output)
add_test(OutputCSVReportTest ${PYTHON_EXECUTABLE}
  ${TEST_PY} OutputTestCase.test_csv_report)
add_test(OutputNUMLReportTest ${PYTHON_EXECUTABLE}
  ${TEST_PY} OutputTestCase.test_numl_report)

# Result related tests
add_test(ResultCSVImportTest ${PYTHON_EXECUTABLE}
  ${TEST_PY} ResultTestCase.test_csv_import)
add_test(ResultNUMLImportTest ${PYTHON_EXECUTABLE}
  ${TEST_PY} ResultTestCase.test_numl_import)