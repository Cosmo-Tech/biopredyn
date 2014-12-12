# Attempt to find jlatexmath-fop.jar

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
