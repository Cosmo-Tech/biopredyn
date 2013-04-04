# Finding csmExternals package
set(TMP_EXT_ROOT $ENV{CSM_EXT_ROOT} )
if(TMP_EXT_ROOT MATCHES NULL)
  find_path(CSMEXTERNALS_DIR NAMES "CMake/cosmo_external_globals.cmake"
    HINTS
    ${CSMEXTERNALS_DIR}
    PATH_SUFFIXES "CMake"
    )
else()
  find_path(CSMEXTERNALS_DIR NAMES "CMake/cosmo_external_globals.cmake"
    HINTS
    ${TMP_EXT_ROOT}
    ${CSMEXTERNALS_DIR}
    PATH_SUFFIXES "CMake"
    )
endif()

if(EXISTS ${CSMEXTERNALS_DIR}/CMake/cosmo_external_globals.cmake)
  set(CSMEXTERNALS_USE_FILE "${CSMEXTERNALS_DIR}/CMake/cosmo_external_globals.cmake" CACHE INTERNAL "")
  set(csmExternals_FOUND TRUE CACHE INTERNAL "")
elseif(csmExternals_FIND_REQUIRED)
  set(CSMEXTERNALS_DIR NOTFOUND CACHE INTERNAL "")
  set(csmExternals_FOUND FALSE CACHE INTERNAL "")
  message(FATAL_ERROR "Could NOT find csmExternals. Check ${CMAKE_BINARY_DIR}${CMAKE_FILES_DIRECTORY}/CMakeError.log for more details.")
endif()
