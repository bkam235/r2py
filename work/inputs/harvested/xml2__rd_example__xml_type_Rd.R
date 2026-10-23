# r2py crawler metadata
# package: xml2
# source_type: rd_example
# topic: xml_type.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xml2\help
# lines: 4

suppressPackageStartupMessages(library(xml2))
x <- read_xml("<foo> a <b /> <![CDATA[ blah]]></foo>")
xml_type(x)
xml_type(xml_contents(x))