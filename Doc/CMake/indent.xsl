<?xml version="1.0" encoding="UTF-8"?>
<!--
  Language: XML
  $Author$
  $Date$
  $Revision$
  $Copyright: [2010-2013] The CoSMo Company, All Rights Reserved $
-->
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:saxon="http://icl.com/saxon">
 <xsl:output method="xml" indent="yes" saxon:indent-spaces="2"/>
 <xsl:strip-space elements="*"/>
 <xsl:template match="/">
   <xsl:copy-of select="."/>
 </xsl:template>
</xsl:stylesheet>

