<?xml version="1.0" encoding="UTF-8"?>
<!--
  Language: XML
  $Author$
  $Date$
  $Revision$
  $Copyright: [2010-2013] The CoSMo Company, All Rights Reserved $
-->
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
  <xsl:output method="xml" indent="yes" encoding="UTF-8"/>
  <xsl:template match="/">
    <files>
      <xsl:for-each select="files/file">
        <xsl:sort select="path"/>
        <file>
          <xsl:apply-templates/>
        </file>
      </xsl:for-each>
    </files>
  </xsl:template>
  <xsl:template match="node()|@*">
    <xsl:copy>
      <xsl:apply-templates select="@*"/>
      <xsl:apply-templates/>
    </xsl:copy>
  </xsl:template>
</xsl:stylesheet>
