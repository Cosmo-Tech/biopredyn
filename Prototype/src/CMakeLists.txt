find_package(LIBSBML REQUIRED)
find_package(LIBBZIP2 REQUIRED)

set( LIBSEDML_VERSION libsedml-0.2.1 )
set( LIBSBMLSIM_VERSION libsbmlsim-1.1.0 )
set( LIBNUML_VERSION libnuml-1.0.1 )

add_subdirectory( ${LIBSEDML_VERSION} )
add_subdirectory( ${LIBSBMLSIM_VERSION} )
add_subdirectory( ${LIBNUML_VERSION} )

if (BPD_GENERATE_LIBBIOPREDYN)
  # Parsing library for biopredyn.xsd based XML files
  add_subdirectory(libBioPreDyn)
endif()