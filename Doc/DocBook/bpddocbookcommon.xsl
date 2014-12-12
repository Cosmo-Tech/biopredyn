<?xml version="1.0" encoding="UTF-8"?>
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
</xsl:attribute-set>
</xsl:stylesheet>
