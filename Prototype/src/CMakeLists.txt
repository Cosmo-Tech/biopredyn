set( LIBSBML_VERSION libsbml-5.10.0 )
set( LIBSBMLSIM_VERSION libsbmlsim-1.1.0 )
set( LIBNUML_VERSION libnuml-1.0.1 )
set( LIBSEDML_VERSION libsedml )
set( COPASI_VERSION copasi )
set( LIBFBC_VERSION libfbc )

# Point to the libsbml src directory
set( LIBSBML_INCLUDE_DIR ${CMAKE_CURRENT_SOURCE_DIR}/${LIBSBML_VERSION}/src )

add_subdirectory( ${LIBSBML_VERSION} )

# Set the name of the compiled SBML library
set( LIBSBML_LIBRARY ${LIBSBML_PREFIX}-static )

add_subdirectory( ${LIBSEDML_VERSION} )
add_subdirectory( ${LIBSBMLSIM_VERSION} )
add_subdirectory( ${LIBNUML_VERSION} )
add_subdirectory( ${COPASI_VERSION} )
add_subdirectory( ${LIBFBC_VERSION} )
