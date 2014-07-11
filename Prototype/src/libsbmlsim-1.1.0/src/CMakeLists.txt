set (SOURCES_COMMON)
set(SOURCES_COMMON ${SOURCES_COMMON}
  ${LIBSBMLSIM_SOURCE_DIR}/src/alg_alter_tree_structure.c
  ${LIBSBMLSIM_SOURCE_DIR}/src/allocated_memory.c
  ${LIBSBMLSIM_SOURCE_DIR}/src/alter_tree_structure.c
  ${LIBSBMLSIM_SOURCE_DIR}/src/assignment_alter_tree_structure.c
  ${LIBSBMLSIM_SOURCE_DIR}/src/bifurcation_analysis.c
  ${LIBSBMLSIM_SOURCE_DIR}/src/check_AST.c
  ${LIBSBMLSIM_SOURCE_DIR}/src/check_math.c
  ${LIBSBMLSIM_SOURCE_DIR}/src/check_num.c
  ${LIBSBMLSIM_SOURCE_DIR}/src/copied_AST.c
  ${LIBSBMLSIM_SOURCE_DIR}/src/count_ode.c
  ${LIBSBMLSIM_SOURCE_DIR}/src/dSFMT.c
  ${LIBSBMLSIM_SOURCE_DIR}/src/ev_alter_tree_structure.c
  ${LIBSBMLSIM_SOURCE_DIR}/src/equation.c
  ${LIBSBMLSIM_SOURCE_DIR}/src/get_equation.c
  ${LIBSBMLSIM_SOURCE_DIR}/src/myASTNode.c
  ${LIBSBMLSIM_SOURCE_DIR}/src/myCompartment.c
  ${LIBSBMLSIM_SOURCE_DIR}/src/myDelay.c
  ${LIBSBMLSIM_SOURCE_DIR}/src/myEvent.c
  ${LIBSBMLSIM_SOURCE_DIR}/src/myEventAssignment.c
  ${LIBSBMLSIM_SOURCE_DIR}/src/myInitialAssignment.c
  ${LIBSBMLSIM_SOURCE_DIR}/src/myParameter.c
  ${LIBSBMLSIM_SOURCE_DIR}/src/myReaction.c
  ${LIBSBMLSIM_SOURCE_DIR}/src/myResult.c
  ${LIBSBMLSIM_SOURCE_DIR}/src/myRule.c
  ${LIBSBMLSIM_SOURCE_DIR}/src/mySpecies.c
  ${LIBSBMLSIM_SOURCE_DIR}/src/mySpeciesReference.c
  ${LIBSBMLSIM_SOURCE_DIR}/src/mySBML_objects.c
  ${LIBSBMLSIM_SOURCE_DIR}/src/output_result.c
  ${LIBSBMLSIM_SOURCE_DIR}/src/prepare_algebraic.c
  ${LIBSBMLSIM_SOURCE_DIR}/src/prepare_reversible_fast_reaction.c
  ${LIBSBMLSIM_SOURCE_DIR}/src/print_node_type.c
  ${LIBSBMLSIM_SOURCE_DIR}/src/print_result_list.c
  ${LIBSBMLSIM_SOURCE_DIR}/src/search_max.c
  ${LIBSBMLSIM_SOURCE_DIR}/src/set_local_para_as_value.c
  )

foreach (directory libsbmlsim math solver util )

	set(dir ${directory})

	file(GLOB temp
			${dir}/*.c
			${dir}/*.h)

	# create source group for IDEs
	source_group(${directory} FILES ${temp})

	# add to sources
	set(SOURCES_COMMON ${SOURCES_COMMON} ${temp})

endforeach()

set (SOURCES_LIB ${SOURCES_COMMON} ${LIBSBMLSIM_SOURCE_DIR}/src/lib_main.c)
set (SOURCES_MAIN ${SOURCES_COMMON} ${LIBSBMLSIM_SOURCE_DIR}/src/main.c)
set (SOURCES_TEST test.c)

set (INSTALL_DOCS)
set (INSTALL_DOCS ${INSTALL_DOCS}
  ${LIBSBMLSIM_SOURCE_DIR}/API.txt
  ${LIBSBMLSIM_SOURCE_DIR}/AUTHORS.txt
  ${LIBSBMLSIM_SOURCE_DIR}/COPYING.txt
  ${LIBSBMLSIM_SOURCE_DIR}/FUNDING.txt
  ${LIBSBMLSIM_SOURCE_DIR}/LICENSE.txt
  ${LIBSBMLSIM_SOURCE_DIR}/LICENSE-dSFMT.txt
  ${LIBSBMLSIM_SOURCE_DIR}/NEWS.txt
  ${LIBSBMLSIM_SOURCE_DIR}/README.txt
  ${LIBSBMLSIM_SOURCE_DIR}/VERSION.txt
  )

include_directories(BEFORE ${LIBSBML_INCLUDE_DIR})
include_directories(BEFORE "${LIBSBMLSIM_SOURCE_DIR}/src/libsbmlsim")

# Static library (only for UNIX)
#if(NOT MSVC)
  add_library(sbmlsim-static STATIC ${SOURCES_LIB})
  target_link_libraries(sbmlsim-static ${LIBSBML_PREFIX}-static)
#endif()

# Shared library
add_library(sbmlsim SHARED ${SOURCES_LIB})
target_link_libraries(sbmlsim ${LIBSBML_PREFIX})

# Test program
add_executable(test ${SOURCES_TEST})
target_link_libraries(test sbmlsim ${LIBSBML_PREFIX})

# Simulator for test suiteprogram
add_executable(simulateSBML ${SOURCES_MAIN})
target_link_libraries(simulateSBML sbmlsim-static ${LIBSBML_PREFIX})

# Install targets
INSTALL(TARGETS simulateSBML sbmlsim-static sbmlsim
  RUNTIME DESTINATION bin
  LIBRARY DESTINATION lib
  ARCHIVE DESTINATION lib
  )

# Install include files
FILE(GLOB include_files "${LIBSBMLSIM_SOURCE_DIR}/src/libsbmlsim/*.h")
INSTALL(FILES ${include_files} DESTINATION include/libsbmlsim)
# Install documents
INSTALL(FILES ${INSTALL_DOCS} DESTINATION share/libsbmlsim)
# Install sample SBML, result files
FILE(GLOB sample_files "${LIBSBMLSIM_SOURCE_DIR}/examples/sample.*")
INSTALL(FILES ${sample_files} DESTINATION share/libsbmlsim)
# Install C and C++ code
INSTALL(FILES ${LIBSBMLSIM_SOURCE_DIR}/examples/c/test.c ${LIBSBMLSIM_SOURCE_DIR}/examples/c/Makefile DESTINATION share/libsbmlsim/c)
INSTALL(FILES ${LIBSBMLSIM_SOURCE_DIR}/examples/cpp/test.cpp ${LIBSBMLSIM_SOURCE_DIR}/examples/cpp/Makefile DESTINATION share/libsbmlsim/cpp)
# Install dependent libraries on Windows
if(MSVC)
  FILE(GLOB windows_depend_dlls "${LIBSBMLSIM_SOURCE_DIR}/depend/bin/*.dll")
  INSTALL(FILES ${windows_depend_dlls} DESTINATION bin)
  INSTALL(FILES ${LIBSBMLSIM_SOURCE_DIR}/README.txt DESTINATION .)
endif()

# Bindings
if(WITH_JAVA)
add_subdirectory(bindings/java)
endif()

if(WITH_PYTHON)
add_subdirectory(bindings/python)
endif()

if(WITH_PERL)
add_subdirectory(bindings/perl)
endif()

if(WITH_RUBY)
add_subdirectory(bindings/ruby)
endif()

if(WITH_CSHARP)
add_subdirectory(bindings/csharp)
endif()

# for installer
INCLUDE(InstallRequiredSystemLibraries)                                                                                                                                           

SET(CPACK_PACKAGE_DESCRIPTION "LibSBMLSim")
SET(CPACK_PACKAGE_DESCRIPTION_SUMMARY "LibSBMLSim: The library for simulating SBML models")
SET(CPACK_PACKAGE_NAME "libsbmlsim")
SET(CPACK_PACKAGE_VENDOR "LibSBMLSim development team")
SET(CPACK_PACKAGE_CONTACT "LibSBMLSim development Team <sbmlsim@fun.bio.keio.ac.jp>")
SET(CPACK_PACKAGE_DESCRIPTION_FILE "${LIBSBMLSIM_SOURCE_DIR}/README.txt")
SET(CPACK_RESOURCE_FILE_LICENSE "${LIBSBMLSIM_SOURCE_DIR}/LICENSE.txt")
SET(CPACK_PACKAGE_VERSION_MAJOR "1")
SET(CPACK_PACKAGE_VERSION_MINOR "1")
SET(CPACK_PACKAGE_VERSION_PATCH "0")
SET(CPACK_PACKAGE_VERSION "${CPACK_PACKAGE_VERSION_MAJOR}.${CPACK_PACKAGE_VERSION_MINOR}.${CPACK_PACKAGE_VERSION_PATCH}")
SET(CPACK_RESOURCE_FILE_README "${LIBSBMLSIM_SOURCE_DIR}/README.txt")
SET(CPACK_RESOURCE_FILE_WELCOME "${LIBSBMLSIM_SOURCE_DIR}/templates/Welcome.txt")

# for Source code archive
SET(CPACK_SOURCE_PACKAGE_FILE_NAME "${CPACK_PACKAGE_NAME}-${CPACK_PACKAGE_VERSION}")
SET(CPACK_SOURCE_GENERATOR "TGZ;ZIP") 
#SET(CPACK_INCLUDE_TOPLEVEL_DIRECTORY "1")
#SET(CPACK_SOURCE_TOPLEVEL_TAG "Source") 
#SET(CPACK_SOURCE_IGNORE_FILES "/CVS/;\\\\.DS_Store;/\\\\.svn/;/\\\\.git/;\\\\.swp$;\\\\.#;.*~;/templates/;/diff/;/simulation_results/;/bindings/;^l?v*;build_.*\\\\.sh;depend-.*\\\\.zip;ev_func_piece\\\\.xml") 
SET(CPACK_SOURCE_IGNORE_FILES 
  "/CVS/;/\\\\.svn/;/\\\\.git/;\\\\.DS_Store;\\\\.swp$"
  "/build/;^bindings/java;^bindings/perl;^bindings/python;/diff/;/simulation_results/"
  "testcases/simulateSBML"
  "testcases/cases/"
  "testcases/.*-results\\\\.csv"
  "testcases/out\\\\.csv"
  "build_csharp\\\\.sh;build_java\\\\.sh;build_python\\\\.sh;depend-.*\\\\.zip;result\\\\.zip"
  "Makefile\\\\.dist;ev_func_piece\\\\.xml;00remove\\\\.sh"
)

# 32bit or 64bit
IF(CMAKE_SIZEOF_VOID_P EQUAL 4)
  SET(CPACK_DEBIAN_PACKAGE_ARCHITECTURE "i386")
  SET(CPACK_RPM_PACKAGE_ARCHITECTURE "i386")
  SET(PACKAGE_ARCH_EXT "x86")
ELSE()
  SET(CPACK_DEBIAN_PACKAGE_ARCHITECTURE "amd64")
  SET(CPACK_RPM_PACKAGE_ARCHITECTURE "x86_64")
  SET(PACKAGE_ARCH_EXT "x64")
ENDIF()

IF(WIN32 AND NOT UNIX)
  SET(CPACK_PACKAGE_INSTALL_DIRECTORY "${CPACK_PACKAGE_NAME}-${CPACK_PACKAGE_VERSION_MAJOR}.${CPACK_PACKAGE_VERSION_MINOR}")
  # There is a bug in NSI that does not handle full unix paths properly. Make
  # sure there is at least one set of four (4) backlasshes.
  #SET(CPACK_PACKAGE_ICON "${CMake_SOURCE_DIR}/Utilities/Release\\\\InstallIcon.bmp")
  #SET(CPACK_NSIS_INSTALLED_ICON_NAME "bin\\\\MyExecutable.exe")
  SET(CPACK_NSIS_DISPLAY_NAME "${CPACK_PACKAGE_INSTALL_DIRECTORY}")
  SET(CPACK_NSIS_HELP_LINK "http:\\\\\\\\fun.bio.keio.ac.jp\\\\software\\\\libsbmlsim")
  SET(CPACK_NSIS_URL_INFO_ABOUT "http:\\\\\\\\bio.keio.ac.jp\\\\software\\\\libsbmlsim")
  SET(CPACK_NSIS_CONTACT "sbmlsim@fun.bio.keio.ac.jp")
  SET(CPACK_NSIS_MODIFY_PATH ON)
ELSE(WIN32 AND NOT UNIX)
  #  SET(CPACK_INCLUDE_TOPLEVEL_DIRECTORY 0)
  SET(CPACK_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")
  SET(CPACK_SET_DESTDIR "ON")
  SET(CPACK_PACKAGE_FILE_NAME ${CPACK_PACKAGE_NAME}-${CPACK_PACKAGE_VERSION}-${CMAKE_SYSTEM_NAME}-${CMAKE_SYSTEM_VERSION}-${PACKAGE_ARCH_EXT})
  IF(${CMAKE_SYSTEM_NAME} MATCHES "Linux")
    SET(CPACK_GENERATOR "DEB")
    SET(CPACK_INSTALL_PREFIX "/usr")
    SET(CPACK_RPM_PACKAGE_LICENSE "LGPL")
    SET(CPACK_RPM_PACKAGE_GROUP "Libraries/Development")
    SET(CPACK_DEBIAN_PACKAGE_PRIORITY "optional")
    SET(CPACK_DEBIAN_PACKAGE_SECTION "Libraries")
    STRING(TOLOWER "${CPACK_PACKAGE_NAME}" CPACK_PACKAGE_NAME_LOWERCASE) 
    SET(CPACK_PACKAGE_FILE_NAME "${CPACK_PACKAGE_NAME_LOWERCASE}_${CPACK_PACKAGE_VERSION}_${CPACK_DEBIAN_PACKAGE_ARCHITECTURE}")   
  ELSEIF(APPLE)
    SET (CPACK_GENERATOR "PackageMaker")
    IF(${CMAKE_SYSTEM_VERSION} MATCHES "^5\\.5") 
      SET(MACOSX_NAME "puma")
    ELSEIF(${CMAKE_SYSTEM_VERSION} MATCHES "^6\\.8") 
      SET(MACOSX_NAME "jaguar")
    ELSEIF(${CMAKE_SYSTEM_VERSION} MATCHES "^7\\.9") 
      SET(MACOSX_NAME "panther")
    ELSEIF(${CMAKE_SYSTEM_VERSION} MATCHES "^8\\.11") 
      SET(MACOSX_NAME "tiger")
    ELSEIF(${CMAKE_SYSTEM_VERSION} MATCHES "^9\\.8") 
      SET(MACOSX_NAME "leopard")
    ELSEIF(${CMAKE_SYSTEM_VERSION} MATCHES "^10\\.8") 
      SET(MACOSX_NAME "snowleopard")
    ELSEIF(${CMAKE_SYSTEM_VERSION} MATCHES "^11\\.4") 
      SET(MACOSX_NAME "lion")
    ELSEIF(${CMAKE_SYSTEM_VERSION} MATCHES "^12\\.0") 
      SET(MACOSX_NAME "mountainlion")
    ELSE()
      SET(MACOSX_NAME "unknown")
    ENDIF()
    SET(CPACK_PACKAGE_FILE_NAME ${CPACK_PACKAGE_NAME}-${CPACK_PACKAGE_VERSION}-macosx-${MACOSX_NAME}-${PACKAGE_ARCH_EXT})
  ENDIF()
  #SET(CPACK_STRIP_FILES "bin/MyExecutable")
  #SET(CPACK_SOURCE_STRIP_FILES "")
ENDIF(WIN32 AND NOT UNIX)

#SET(CPACK_PACKAGE_EXECUTABLES "MyExecutable" "My Executable")
INCLUDE(CPack)
