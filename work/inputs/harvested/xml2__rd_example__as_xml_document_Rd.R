# r2py crawler metadata
# package: xml2
# source_type: rd_example
# topic: as_xml_document.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xml2\help
# lines: 12

suppressPackageStartupMessages(library(xml2))
as_xml_document(list(x = list()))

# Nesting multiple nodes
as_xml_document(list(foo = list(bar = list(baz = list()))))

# attributes are stored as R attributes
as_xml_document(list(foo = structure(list(), id = "a")))
as_xml_document(list(foo = list(
  bar = structure(list(), id = "a"),
  bar = structure(list(), id = "b")
)))