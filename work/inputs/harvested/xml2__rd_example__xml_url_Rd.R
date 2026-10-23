# r2py crawler metadata
# package: xml2
# source_type: rd_example
# topic: xml_url.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xml2\help
# lines: 6

suppressPackageStartupMessages(library(xml2))
catalog <- read_xml(xml2_example("cd_catalog.xml"))
xml_url(catalog)

x <- read_xml("<foo/>")
xml_url(x)