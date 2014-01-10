set(PACKAGE_VERSION 0.1)

add_subdirectory(src)
add_subdirectory(python)
add_subdirectory(testing)

# doxygen generation
if (BPD_GENERATE_DOXYGEN)
  add_subdirectory(doxygen)
endif()