<?xml version="1.0" encoding="UTF-8"?>
<!--
  This XSLT convert a main() doxygen function into a docbook style <programlisting/>
-->
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
  <xsl:output method="xml" indent="yes" encoding="utf-8"/>
  <xsl:template match="doxygen">
    <!--
    <article version="5.0" xmlns="http://docbook.org/ns/docbook"
         xmlns:xlink="http://www.w3.org/1999/xlink"
         xmlns:xi="http://www.w3.org/2001/XInclude"
         xmlns:db="http://docbook.org/ns/docbook">
      -->
      <xsl:apply-templates/>
    <!--
    </article>
    -->
  </xsl:template>
  <xsl:template match="compounddef">
    <section>
      <title>section</title>
      <xsl:apply-templates/>
    </section>
  </xsl:template>
  <xsl:template match="programlisting">
    <para>
      <programlisting>
        <xsl:apply-templates/>
      </programlisting>
    </para>
  </xsl:template>
  <xsl:template match="codeline">
    <xsl:apply-templates/>
  </xsl:template>
  <xsl:template match="innerclass">
  </xsl:template>
  <xsl:template match="compoundname">
  </xsl:template>
  <xsl:template match="memberdef">
  </xsl:template>
  <xsl:template match="briefdescription">
  </xsl:template>
  <xsl:template match="detaileddescription">
  </xsl:template>
  <xsl:template match="location">
    <programlisting>
      <filename>
        <xsl:value-of select="@file"/>
      </filename>
    </programlisting>
  </xsl:template>
  <xsl:template match="collaborationgraph">
  </xsl:template>
  <xsl:template match="sourcecode">
  </xsl:template>
  <xsl:template match="sp">
    <xsl:text> </xsl:text>
  </xsl:template>
  <xsl:template match="highlight[@class='keywordtype']">
    <type>
      <xsl:apply-templates/>
    </type>
  </xsl:template>
  <xsl:template match="highlight[@class='comment']">
    <lineannotation>
      <xsl:apply-templates/>
    </lineannotation>
  </xsl:template>
  <xsl:template match="highlight[@class='keywordflow']">
    <xsl:choose>
      <xsl:when test=".='return'">
        <!--returnvalue-->
        <xsl:apply-templates/>
        <!--/returnvalue-->
      </xsl:when>
      <xsl:otherwise>
        <xsl:apply-templates/>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>
</xsl:stylesheet>
