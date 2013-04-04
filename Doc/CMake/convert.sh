# This script takes in an original html file, tidy it into (valid) xhtml, then converts it to docbook

# See basic docbook documentation at:
# http://supportweb.cs.bham.ac.uk/documentation/tutorials/docsystem/build/tutorials/UniDocBook/UniDocBook.html
check_exit_value()
{
   VALUE="$1"
   if [ "$VALUE" != "0" ]; then
    echo "error in $2"
    exit 1
   fi      
}

filename=$1
filename_html=`echo $filename | sed -e 's@Specifications@CoSMo/ReferenceGuide@'`
echo $filename_html
dirname=`dirname $filename_html`
echo $dirname
mkdir -p $dirname
filename_xhtml=`echo $filename_html | sed -e 's/\.html/\.xhtml/'`
echo $filename_xhtml
filename_xml=`echo $filename_html | sed -e 's/\.html/\.xml/'`
echo $filename_xml
#svn cp $filename1 $filename3
#cp $filename1 $filename3
tidy -config tidy.config -o $filename_xhtml $filename
#check_exit_value $? "tidy did not return properly" || exit 1
#EXIT STATUS
#       0      All input files were processed successfully.
#       1      There were warnings.
#       2      There were errors.
if [ "$?" = "2" ]; then
  echo "error in tidy"
  exit 1
fi      

# Check generated XHTML
xmllint --noout --nonet --valid $filename_xhtml

## Version #1
## Using herold (dbdoclet.org)
##herold --in $filename_xhtml --out $filename_xml --title toto
#java -jar herold_5.2.4.jar -i $filename_xhtml -o $filename_xml
## title does not work
##herold --in $filename_xhtml --out $filename_xml --decompose-tables
#herold --in $filename_xhtml --out $filename_xml
#check_exit_value $? "herold did not return properly" || exit 1
## For some reason herold does not set the correct version for docbook 5
## using:
## herold Version 5.2.2 P129 2010-01-28 14:35
## Fixing number
#sed -i -e 's/article version="1.0"/article version="5.0"/' $filename_xml

# Version #2
xsltproc -o $filename_xml /home/mathieu/Projects/csm/Workgroup/Mathieu/docbook/html2docbook.xsl $filename_xhtml 
#xsltproc -o $filename_xml /usr/share/xml/docbook/stylesheet/docbook5/db4-upgrade.xsl $filename_xml.tmp

# Version #3
#xsltproc -o $filename_xml xhtml2docbook.xsl $filename_xhtml 


# Let's check this is valid docbook 5 document:
#xmllint --noout --schema /usr/share/xml/docbook/schema/xsd/5.0/docbook.xsd $filename_xml

# double-check and reconvert to HTML
#xmlto html-nochunks $filename_xml
#xsltproc -o $filename_html /usr/share/xml/docbook/stylesheet/docbook-xsl-ns/fo/docbook.xsl $filename_xml
#xsltproc -o $filename_html /usr/share/xml/docbook/stylesheet/docbook-xsl-ns/html/docbook.xsl $filename_xml

#xmllint --format --output $filename_xml.clean $filename_xml
