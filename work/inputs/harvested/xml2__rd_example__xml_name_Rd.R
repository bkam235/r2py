# r2py crawler metadata
# package: xml2
# source_type: rd_example
# topic: xml_name.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xml2\help
# lines: 7

suppressPackageStartupMessages(library(xml2))
x <- read_xml("<bar>123</bar>")
xml_name(x)

y <- read_xml("<bar><baz>1</baz>abc<foo /></bar>")
z <- xml_children(y)
xml_name(xml_children(y))