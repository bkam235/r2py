# r2py crawler metadata
# package: xml2
# source_type: rd_example
# topic: xml_cdata.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xml2\help
# lines: 4

suppressPackageStartupMessages(library(xml2))
x <- xml_new_root("root")
xml_add_child(x, xml_cdata("<d/>"))
as.character(x)