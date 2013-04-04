<?xml version='1.0' encoding="utf-8"?>
<!--
  Language: XML
  $Author$
  $Date$
  $Revision$
  $Copyright: [2010-2013] The CoSMo Company, All Rights Reserved $
-->
<xsl:stylesheet
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">

<xsl:import href="/usr/share/xml/docbook/stylesheet/docbook-xsl/html/docbook.xsl"/>
<xsl:import href="/usr/share/xml/docbook/stylesheet/docbook-xsl/highlighting/common.xsl"/>
<xsl:import href="/usr/share/xml/docbook/stylesheet/docbook-xsl/html/highlight.xsl"/>

<!--xsl:param name="html.stylesheet" select="'corpstyle.css'"/-->
<xsl:param name="highlight.source" select="1"/>

<!-- does not work: -->
<!--xsl:param name="highlight.xslthl.config" select="/home/mathieu/Software/xslthl/highlighters/xslthl-config.xml"/-->
<!-- does not work: -->
<!--xsl:param name="highlight.xslthl.config" select="/home/mathieu/Software/xslthl/highlighters/xslthl-config.xml"/-->
<!--xsl:param name="highlight.xslthl.config" select="'/home/mathieu/Software/xslthl/highlighters/xslthl-config.xml'"/-->
<xsl:param name="highlight.xslthl.config">file:///usr/share/xslthl/highlighters/xslthl-config.xml</xsl:param>

<!-- Instead you have to use the command line solution:

$ java -classpath /usr/share/java/saxon.jar:/home/mathieu/Software/xslthl/xslthl-2.0.1.jar  -Dxslthl.config="file:////home/mathieu/Software/xslthl/highlighters/xslthl-config.xml"  com.icl.saxon.StyleSheet  -o myfile.html /home/mathieu/Projects/csm/Doc/Corporate/Training/WritingDocumentationInDocbook.xml myhtml.xsl


with

$ ls -al /home/mathieu/Software/xslthl
total 48
drwxr-xr-x  3 mathieu mathieu   144 2010-02-22 10:40 ./
drwxr-xr-x 49 mathieu mathieu  3664 2010-02-22 10:40 ../
drwxr-xr-x  2 mathieu mathieu   536 2010-02-22 10:57 highlighters/
-rw-r- r-   1 mathieu mathieu  1138 2008-07-09 16:31 LICENSE.txt
-rw-r- r-   1 mathieu mathieu 37890 2009-01-23 20:14 xslthl-2.0.1.jar


Ref:

http://www.sagehill.net/docbookxsl/CustomMethods.html
http://docbook.xml-doc.org/snapshots/xsl/doc/html/highlight.source.html
https://sourceforge.net/apps/mediawiki/xslthl/index.php?title=Usage
http://docbook.sourceforge.net/release/xsl/current/doc/fo/highlight.source.html
http://www.sagehill.net/docbookxsl/SyntaxHighlighting.html

-->

</xsl:stylesheet>

