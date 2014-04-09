<?xml version="1.0" encoding="utf-8"?>
<!--
  Language: XML
  $Author$
  $Date$
  $Revision$
  $Copyright: [2010-2014] The CoSMo Company, All Rights Reserved $
-->

<!--+
    |  ascii-art.xsl v1.0
    |
    |  XSLT Stylesheet to provide an ASCII-art rendition of a DocBook file's
    |  structure.  Example use:
    |
    |      xsltproc ascii-art.xsl docbook-file.xml
    |
    |  Some large documents are broken into several files, which are combined
    |  using XInclude.  If so, then each file may be converted independently or
    |  the overall document shown if xsltproc's xinclude option is enabled.
    |
    |  There are several parameters to adjust the output:
    |
    |    initial-indent    text to prefix each line of output.  The default
    |                      value is two spaces.
    |
    |    max-line-length   the maximum line length.  The default value is
    |                      75.
    |
    |    ellipsis          the text appended to a line to indicate it has been
    |                      truncated.
    |
    |    item-with-new-item              These three items provide the ASCII-
    |    item-with-following-sibling     art elements that are used to build
    |    item-without-following-sibling  the tree structure.
    |
    |  Copyright (c) 2010, Paul Millar <paul.millar@desy.de>
    |  All rights reserved.
    |
    |  Redistribution and use in source and binary forms, with or without
    |  modification, are permitted provided that the following conditions
    |  are met:
    |
    |      * Redistributions of source code must retain the above copyright
    |        notice, this list of conditions and the following disclaimer.
    |      * Redistributions in binary form must reproduce the above copyright
    |        notice, this list of conditions and the following disclaimer in
    |        the documentation and/or other materials provided with the
    |        distribution.
    |      * None of the names of contributors may be used to endorse or
    |        promote products derived from this software without specific
    |        prior written permission.
    |
    |  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
    |  IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
    |  TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
    |  PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
    |  HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
    |  SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
    |  TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
    |  PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
    |  LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
    |  NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
    |  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
    |
    |  Please email any bug-fixes to Paul Millar <paul.millar@desy.de>
    +-->

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                version="1.0">

<xsl:param name="initial-indent" select="'  '"/>
<xsl:param name="max-line-length" select="'75'"/>
<xsl:param name="ellipsis" select="'[...]'"/>

<xsl:param name="item-with-new-item"             select="' +--'"/>
<xsl:param name="item-with-following-sibling"    select="' |  '"/>
<xsl:param name="item-without-following-sibling" select="'    '"/>

<xsl:variable name="ellipsis-length" select="string-length($ellipsis)"/>
<xsl:variable name="item-length" select="string-length($item-with-new-item)"/>

<xsl:output method="text" media-type="text/plain"/>

<xsl:template match="/">
  <xsl:if test="string-length($item-with-following-sibling) != $item-length or
                string-length($item-without-following-sibling) != $item-length">
    <xsl:message>Warning: the ASCII art fragments must have the same
    length.</xsl:message>
  </xsl:if>

  <xsl:apply-templates select="*"/>
</xsl:template>


<xsl:template match="node()" mode="have-interesting-item"/>
<xsl:template match="book|preface|article|part|chapter|appendix|section|tip|note|important|warning|caution"
        mode="have-interesting-item">
  <xsl:text>Y</xsl:text>
</xsl:template>


<xsl:template match="book|preface|article|part|chapter|appendix|section|tip|note|important|warning|caution">

  <xsl:variable name="have-preceding">
    <xsl:apply-templates select="preceding-sibling::*"
       mode="have-interesting-item"/>
  </xsl:variable>

  <xsl:if test="not(normalize-space($have-preceding))">
    <xsl:call-template name="emit-empty-line-with-indent">
      <xsl:with-param name="has-following-sibling" select="true()"/>
    </xsl:call-template>
  </xsl:if>

  <xsl:if test="not(ancestor::*)">
    <xsl:value-of select="$initial-indent"/>
  </xsl:if>

  <xsl:apply-templates select="ancestor::*[1]" mode="emit-indent">
    <xsl:with-param name="has-new-item" select="true()"/>
  </xsl:apply-templates>

  <xsl:call-template name="emit-title-label"/>

  <xsl:apply-templates select="*"/>

  <xsl:variable name="have-following">
    <xsl:apply-templates select="following-sibling::*"
       mode="have-interesting-item"/>
  </xsl:variable>

  <xsl:variable name="have-children">
    <xsl:apply-templates select="child::*" mode="have-interesting-item"/>
  </xsl:variable>

  <xsl:if test="not(normalize-space($have-following)) and
                not(normalize-space($have-children))">
    <xsl:call-template name="emit-empty-line-with-indent"/>
  </xsl:if>
</xsl:template>

<xsl:template match="node()"/>


<xsl:template name="emit-empty-line-with-indent">
  <xsl:param name="has-following-sibling" select="false()"/>

  <xsl:apply-templates select="ancestor::*[1]" mode="emit-indent">
    <xsl:with-param name="has-following-sibling"
        select="$has-following-sibling"/>
  </xsl:apply-templates>

  <xsl:text>&#xa;</xsl:text>
</xsl:template>


<xsl:template match="*" mode="emit-indent">
  <xsl:param name="so-far"/>
  <xsl:param name="has-new-item" select="false()"/>
  <xsl:param name="has-following-sibling" select="false()"/>

  <xsl:variable name="this-item">
    <xsl:choose>
      <xsl:when test="$has-new-item">
  <xsl:value-of select="$item-with-new-item"/>
      </xsl:when>
      <xsl:when test="$has-following-sibling">
  <xsl:value-of select="$item-with-following-sibling"/>
      </xsl:when>
      <xsl:otherwise>
  <xsl:value-of select="$item-without-following-sibling"/>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:variable>

  <xsl:variable name="next-item" select="concat($this-item, $so-far)"/>

  <xsl:variable name="has-following">
    <xsl:apply-templates select="following-sibling::*" mode="have-interesting-item"/>
  </xsl:variable>

  <xsl:choose>
    <xsl:when test="count(ancestor::*) > 0">
      <xsl:apply-templates select="ancestor::*[1]" mode="emit-indent">
  <xsl:with-param name="so-far" select="$next-item"/>
  <xsl:with-param name="has-following-sibling"
      select="boolean(normalize-space($has-following))"/>
      </xsl:apply-templates>
    </xsl:when>

    <xsl:otherwise>
      <xsl:value-of select="concat($initial-indent, $next-item)"/>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>


<!-- Emit something like "chapter: This is the chapter title" but truncate the
     line if it's too long -->
<xsl:template name="emit-title-label">

  <xsl:variable name="title">
    <xsl:call-template name="emit-title"/>
  </xsl:variable>

  <xsl:variable name="indent-length"
    select="string-length($initial-indent) +
      count(ancestor::*) * $item-length"/>

  <xsl:variable name="line-length"
    select="$indent-length + string-length($title)"/>

  <xsl:choose>
    <xsl:when test="$line-length > $max-line-length">
      <xsl:variable name="trunc-title-length"
        select="$max-line-length - $indent-length - $ellipsis-length"/>
      <xsl:value-of select="concat(substring($title, 1, $trunc-title-length), $ellipsis, '&#xa;')"/>
    </xsl:when>

    <xsl:otherwise>
      <xsl:value-of select="concat($title, '&#xa;')"/>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>


<!-- Emit something like "chapter: The chapter title" -->
<xsl:template name="emit-title">
  <xsl:choose>
    <xsl:when test="title">
      <xsl:value-of select="concat(name(), ': ', normalize-space(title[1]))"/>
    </xsl:when>

    <xsl:when test="para">
      <xsl:value-of select="concat(name(), ': ', normalize-space(para[1]))"/>
    </xsl:when>

    <xsl:otherwise>
      <xsl:value-of select="name()"/>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>

</xsl:stylesheet>
