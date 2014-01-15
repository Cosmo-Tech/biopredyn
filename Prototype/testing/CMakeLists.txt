# Opens a file and test whether it is SBML compliant
add_test(SBMLComplianceTest ${PYTHON_EXECUTABLE}
  ${CMAKE_CURRENT_SOURCE_DIR}/test.py
  --sbml ${CMAKE_CURRENT_SOURCE_DIR}/../data/FEBS.xml)

# Opens a file, test whether it is SED-ML compliant, execute it, display
# graphical output
add_test(GraphicalOutputTest ${PYTHON_EXECUTABLE}
  ${CMAKE_CURRENT_SOURCE_DIR}/test.py
  --sedml ${CMAKE_CURRENT_SOURCE_DIR}/FEBS_test_graphical_output.xml)

# Opens a file, test whether it is SED-ML compliant, execute it, write a CSV
# report
add_test(CSVReportTest ${PYTHON_EXECUTABLE}
  ${CMAKE_CURRENT_SOURCE_DIR}/test.py
  --sedml ${CMAKE_CURRENT_SOURCE_DIR}/FEBS_test_report.xml
  -o ${CMAKE_CURRENT_BINARY_DIR}/test_output.csv)

# Opens a file, test whether it is SED-ML compliant, execute it, write a NuML
# report
add_test(NuMLReportTest ${PYTHON_EXECUTABLE}
  ${CMAKE_CURRENT_SOURCE_DIR}/test.py
  --sedml ${CMAKE_CURRENT_SOURCE_DIR}/FEBS_test_report.xml
  -o ${CMAKE_CURRENT_BINARY_DIR}/test_output.xml)

# Opens a NuML result file and plot its content with matplotlib.
add_test(NuMLFileImportTest ${PYTHON_EXECUTABLE}
  ${CMAKE_CURRENT_SOURCE_DIR}/test.py
  --numl ${CMAKE_CURRENT_SOURCE_DIR}/../data/FEBS_numerical_data.xml)