import lxml.etree as ET
import sys

args = sys.argv[1:]
xml_filename = args[0]
xsl_filename = "transform-greek-xml.xsl"

dom = ET.parse(xml_filename)
xslt = ET.parse(xsl_filename)
transform = ET.XSLT(xslt)
newdom = transform(dom)
datastr = ET.tostring(newdom, pretty_print=True)

print(datastr)

with open(args[1], 'w', encoding='utf-8') as f:
    f.write("<html><head><link rel=\"stylesheet\" type=\"text/css\" href=\"commentcss.css\"></head>\n")
    f.write(str(datastr, 'utf-8')) 
    f.write("\n</html>")

print("done!")

