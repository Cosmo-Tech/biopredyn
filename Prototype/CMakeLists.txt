set(PACKAGE_VERSION 0.1)

add_subdirectory(src)
add_subdirectory(python)

# doxygen generation
if (BPD_GENERATE_DOXYGEN)
  add_subdirectory(doxygen)
endif()