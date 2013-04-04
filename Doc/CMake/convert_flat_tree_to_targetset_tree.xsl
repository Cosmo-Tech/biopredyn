<?xml version="1.0" encoding="utf-8"?>
<!--
  Language: XML
  $Author$
  $Date$
  $Revision$
  $Copyright: [2010-2013] The CoSMo Company, All Rights Reserved $
-->
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
  <xsl:output method="xml" indent="yes" encoding="UTF-8"/>
  <!--

  The goal of this XSL script is to transform a usual installation path

  eg.:
    share/doc/Corporate/Training/BuildQtApplicationsWithCMake/index.html
    share/doc/Corporate/Training/VirtualBox.pdf

  That is generally computed by build system (eg. CMake), and to convert
  that flat string (flat directory structure) into a full targetset structure
  that is used when doing olinks. This script goes over all path and detect
  common subdirectory so that:

  <dir name="share">
    <dir name="doc">
      <dir name="Corporate">
        <dir name="Training">
          <document targetdoc="BuildQtApplicationsWithCMake"/>
          <document targetdoc="VirtualBox"/>
        </dir>
      </dir>
    </dir>
  </dir>

  See for more info:
  * http://www.sagehill.net/docbookxsl/Olinking.html
  * http://www.sagehill.net/docbookxsl/OlinkVariations.html

  -->
  <!--
  Implementation details:
  We are generating the Xinclude version of the sitemap file, since xslt is poorly define
  when generating DOCTYPE. Since we are internally using Xinclude, this does not add any
  specific new requirement.

  MM 09/07/2010. I cannot find a PUBLIC identifier for targetset. Therefore
  I cannot validate the generated document. The only SYSTEM identifier I could find is:
  <!DOCTYPE targetset
    SYSTEM "file:///usr/share/xml/docbook/stylesheet/docbook-xsl/common/targetdatabase.dtd">
  This is not portable.

Ref:
http://www.biglist.com/lists/xsl-list/archives/200408/msg00858.html
-->
  <!--
Here's a set of templates that works with your example.

The main template is the transformDocument template. This takes a path
(an initial part of a path) and a set of items (whose paths should all
start with the $path). It works out the next step in the path for the
first item and from that creates a new path. Then it sorts the items
into three groups:

  - items whose path *is* the new path, which should just be output
  - items whose path *starts with* the new path, which need to be
    processed again by this template, with the new path
  - items whose path *doesn't* start with the new path, which need to
    be processed again by this template, with the current path

The result of the first two of these groups gets put within a <path>
element, and the result of the third of these groups gets inserted
afterwards.
-->
  <xsl:template name="get-filename">
    <xsl:param name="path"/>
    <xsl:choose>
      <xsl:when test="contains( $path, '/' )">
        <xsl:call-template name="get-filename">
          <xsl:with-param name="path" select="substring-after( $path, '/' )"/>
        </xsl:call-template>
      </xsl:when>
      <xsl:otherwise>
        <xsl:value-of select="$path"/>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>
  <xsl:template name="transformDocument">
    <xsl:param name="path"/>
    <xsl:param name="files" select="/.."/>
    <xsl:if test="$files">
      <xsl:variable name="rest" select="substring-after($files[1]/path, concat($path, '/'))"/>
      <xsl:variable name="step">
        <xsl:choose>
          <xsl:when test="contains($rest, '/')">
            <xsl:value-of select="substring-before($rest, '/')"/>
          </xsl:when>
          <xsl:otherwise>
            <xsl:value-of select="$rest"/>
          </xsl:otherwise>
        </xsl:choose>
      </xsl:variable>
      <xsl:variable name="newPath" select="concat($path, '/', $step)"/>
      <xsl:choose>
        <xsl:when test="contains($rest, '/')">
          <dir name="{$step}">
            <xsl:apply-templates select="$files[path = $newPath]">
              <!--xsl:sort select="file/path"/-->
            </xsl:apply-templates>
            <xsl:call-template name="transformDocument">
              <xsl:with-param name="path" select="$newPath"/>
              <xsl:with-param name="files" select="$files[starts-with(path, $newPath) and path != $newPath]"/>
            </xsl:call-template>
          </dir>
        </xsl:when>
        <xsl:otherwise>
          <!--only one token left-->
          <xsl:variable name="token" select="$step"/>
          <xsl:variable name="prev-token">
            <xsl:call-template name="get-filename">
              <xsl:with-param name="path" select="$path"/>
            </xsl:call-template>
          </xsl:variable>
          <xsl:choose>
            <xsl:when test="contains($token, 'html')">
              <!--document targetdoc="{$prev-token}" baseuri="{$token}"-->
              <document targetdoc="{$prev-token}" >
                <xi:include xmlns:xi="http://www.w3.org/2001/XInclude" href="{$prev-token}.olinkdb.html.xml"/>
              </document>
            </xsl:when>
            <xsl:when test="contains($token, 'pdf')">
              <xsl:variable name="basename" select="substring-before($token,'.pdf')"/>
              <!-- TODO
              http://cygwin.ru/ml/docbook-apps/2005-q2/msg00220.html
              http://www.mail-archive.com/fop-dev@xmlgraphics.apache.org/msg06568.html
              http://xmlgraphics.apache.org/fop/0.95/extensions.html#bookmarks
              -->
              <!-- https://www.thecosmocompany.com/doc/Corporate/Training/CoSMoValidation.pdf -->
              <xsl:variable name="myurl" select="substring-after($path,'share')"/>
              <!--document targetdoc="{$basename}" baseuri="{concat('https://www.thecosmocompany.com',$myurl,'/',$token)}"-->
              <document targetdoc="{$basename}" baseuri="{$token}">
                <xi:include xmlns:xi="http://www.w3.org/2001/XInclude" href="{$basename}.olinkdb.pdf.xml"/>
              </document>
            </xsl:when>
            <xsl:otherwise>
              <xsl:message>Problem with :(<xsl:value-of select="$token"/>)
        </xsl:message>
            </xsl:otherwise>
          </xsl:choose>
        </xsl:otherwise>
      </xsl:choose>
      <xsl:call-template name="transformDocument">
        <xsl:with-param name="path" select="$path"/>
        <xsl:with-param name="files" select="$files[not(starts-with(path, $newPath))]"/>
      </xsl:call-template>
    </xsl:if>
  </xsl:template>
  <!--
The next template matches the <files> element and starts off the
processing. I've assumed that there's only one root here.
-->
  <xsl:template match="files">
    <xsl:comment>
  THIS IS A GENERATED FILE DO NOT EDIT
</xsl:comment>
    <targetset>
      <targetsetinfo>
    Description of this target database document,
    which is for the examples in olink doc.
  </targetsetinfo>
      <sitemap>
        <xsl:variable name="root" select="substring-before(file[1]/path, '/')"/>
        <dir name="{$root}">
          <xsl:call-template name="transformDocument">
            <xsl:with-param name="path" select="$root"/>
            <xsl:with-param name="files" select="file"/>
          </xsl:call-template>
        </dir>
      </sitemap>
    </targetset>
  </xsl:template>
</xsl:stylesheet>
