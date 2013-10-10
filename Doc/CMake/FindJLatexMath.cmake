# Attempt to find jlatexmath-fop.jar there is no need to find it on windows since FOP_HYPHENATION_PATH is already set by
# the externals.

if(NOT WIN32)
  find_file(
    JLATEXMATH_JAR_PATH
    jlatexmath-fop.jar
    # debian
    /usr/share/java/
    # local installation
    /usr/share/local/java/
    )
endif()
