# r2py crawler metadata
# package: xml2
# source_type: rd_example
# topic: xml_comment.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xml2\help
# lines: 5

suppressPackageStartupMessages(library(xml2))
x <- xml_new_document()
r <- xml_add_child(x, "root")
xml_add_child(r, xml_comment("Hello!"))
as.character(x)