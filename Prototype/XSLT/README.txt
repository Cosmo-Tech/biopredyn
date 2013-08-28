This folder contains XSLT files used for formatting SED-ML files, mainly
cleaning unwanted annotations left by third party SED-ML editors, such as
CellDesigner or SED-ED. They can be used as follows:

xsltproc /path/to/xslt/tree.xsl /path/to/source/tree.xml > /path/to/result/tree.xml