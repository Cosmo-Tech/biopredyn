<?xml version="1.0" encoding="UTF-8"?>
<!--
  Language: XML
  $Author$
  $Date$
  $Revision$
  $Copyright: [2010-2013] The CoSMo Company, All Rights Reserved $
-->
<!--
This files contains the common dodbook setting for the entire CoSMo DocBook documentation
it should not contains CMake variable, but only docbook parameters common to both HTML and PDF output
-->
<xsl:stylesheet
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xslthl="http://xslthl.sf.net"
    xmlns:fo="http://www.w3.org/1999/XSL/Format"
exclude-result-prefixes="xslthl"
version="1.0">
<xsl:output method="xml" indent="no" encoding="UTF-8"/>

<xsl:param name="callout.graphics" select="0"/>
<xsl:param name="callout.unicode" select="1"/>
<xsl:param name="callouts.extension" select="1"/>
<xsl:param name="textinsert.extension" select="1"/>

<xsl:param name="highlight.source" select="1"/>
<xsl:param name="current.docid" select="/*/@id"/>
<xsl:param name="paper.type">A4</xsl:param>

<!-- http://www.sagehill.net/docbookxsl/FormalTitles.html -->
<xsl:param name="formal.title.placement">
figure after
example before
equation after
table before
procedure before
</xsl:param>

<xsl:attribute-set name="monospace.verbatim.properties">
    <xsl:attribute name="wrap-option">wrap</xsl:attribute>
    <!--xsl:attribute name="hyphenation-character">\</xsl:attribute-->
</xsl:attribute-set>

<!-- deprecated-->
<!--xsl:param name="shade.verbatim" select="1"></xsl:param-->

<!--xsl:param name="ignore.image.scaling" select="1"/-->


<!--
<xsl:attribute-set name="figure.properties">
  <xsl:attribute name="text-align">center</xsl:attribute>
</xsl:attribute-set>
-->


</xsl:stylesheet>
