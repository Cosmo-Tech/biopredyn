find_package(LIBSBML REQUIRED)

add_subdirectory(libsedml)
add_subdirectory(libsbmlsim-1.1.0)
add_subdirectory(libnuml)

if (BPD_GENERATE_LIBBIOPREDYN)
  # Parsing library for biopredyn.xsd based XML files
  add_subdirectory(libBioPreDyn)
endif()