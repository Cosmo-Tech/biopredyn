find_package(LIBBZIP2 REQUIRED)

set( LIBSBML_VERSION libsbml-5.8.0 )
set( LIBSBMLSIM_VERSION libsbmlsim-1.1.0 )
set( LIBNUML_VERSION libnuml-1.0.1 )
set( LIBSEDML_VERSION libsedml-0.2.1 )

# Point to the libsbml src directory
set( LIBSBML_INCLUDE_DIR ${CMAKE_CURRENT_SOURCE_DIR}/${LIBSBML_VERSION}/src )

add_subdirectory( ${LIBSBML_VERSION} )
add_subdirectory( ${LIBSEDML_VERSION} )
add_subdirectory( ${LIBSBMLSIM_VERSION} )
add_subdirectory( ${LIBNUML_VERSION} )

if (BPD_GENERATE_LIBBIOPREDYN)
  # Parsing library for biopredyn.xsd based XML files
  add_subdirectory(libBioPreDyn)
endif()