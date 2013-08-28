<?xml version="1.0" encoding="utf-8" ?>
<!--

  -->
<xsl:stylesheet xmlns:sed="http://sed-ml.org/"
		xmlns:sbsi="http://www.sedml.sbsi.editor/level1"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                exclude-result-prefixes="sed"
		version="1.0" >
                
  <xsl:template match="@*|node()">
      <xsl:copy>
          <xsl:apply-templates select="@*|node()"/>
      </xsl:copy>
  </xsl:template>

  <xsl:template match="sed:annotation[count(*)=0]">
    <xsl:apply-templates select="sed:annotation"/>
  </xsl:template>

  <xsl:output method="xml" encoding="UTF-8"/>

</xsl:stylesheet>
