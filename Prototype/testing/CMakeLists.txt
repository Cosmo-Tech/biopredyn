# Opens a SBML file and test whether it is SBML compliant
add_test(SBMLComplianceTest ${PYTHON_EXECUTABLE}
  ${CMAKE_CURRENT_SOURCE_DIR}/test.py
  --sbml ${CMAKE_CURRENT_SOURCE_DIR}/../data/FEBS.xml)

# Imports a model from BioModels and simulate it
add_test(BioModelsImportTest ${PYTHON_EXECUTABLE}
  ${CMAKE_CURRENT_SOURCE_DIR}/test.py
  --sedml ${CMAKE_CURRENT_SOURCE_DIR}/FEBS_test_URN_model.xml)

# Displays the result of a work flow as a 2D plot
add_test(GraphicalOutputTest ${PYTHON_EXECUTABLE}
  ${CMAKE_CURRENT_SOURCE_DIR}/test.py
  --sedml ${CMAKE_CURRENT_SOURCE_DIR}/FEBS_test_graphical_output.xml)

# Displays the result of a work flow as a 3D plot
add_test(GraphicalOutput3DTest ${PYTHON_EXECUTABLE}
  ${CMAKE_CURRENT_SOURCE_DIR}/test.py
  --sedml ${CMAKE_CURRENT_SOURCE_DIR}/FEBS_test_3D_graphical_output.xml)

# Opens a CSV result file and plot its content with matplotlib.
add_test(CSVFileImportTest ${PYTHON_EXECUTABLE}
  ${CMAKE_CURRENT_SOURCE_DIR}/test.py
  --csv ${CMAKE_CURRENT_SOURCE_DIR}/3D_data.csv)

# Exports the result of a work flow as a CSV report
add_test(CSVReportTest ${PYTHON_EXECUTABLE}
  ${CMAKE_CURRENT_SOURCE_DIR}/test.py
  --sedml ${CMAKE_CURRENT_SOURCE_DIR}/FEBS_test_report.xml
  -o ${CMAKE_CURRENT_BINARY_DIR}/test_output.csv)

# Exports the result of a work flow as a NuML result file
add_test(NuMLReportTest ${PYTHON_EXECUTABLE}
  ${CMAKE_CURRENT_SOURCE_DIR}/test.py
  --sedml ${CMAKE_CURRENT_SOURCE_DIR}/FEBS_test_report.xml
  -o ${CMAKE_CURRENT_BINARY_DIR}/test_output.xml)

# Opens a NuML result file and plot its content with matplotlib.
add_test(NuMLFileImportTest ${PYTHON_EXECUTABLE}
  ${CMAKE_CURRENT_SOURCE_DIR}/test.py
  --numl ${CMAKE_CURRENT_SOURCE_DIR}/../data/FEBS_numerical_data.xml)