# r2py crawler metadata
# package: xml2
# source_type: rd_example
# topic: xml_validate.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xml2\help
# lines: 5

suppressPackageStartupMessages(library(xml2))
# Example from https://msdn.microsoft.com/en-us/library/ms256129(v=vs.110).aspx
doc <- read_xml(system.file("extdata/order-doc.xml", package = "xml2"))
schema <- read_xml(system.file("extdata/order-schema.xml", package = "xml2"))
xml_validate(doc, schema)