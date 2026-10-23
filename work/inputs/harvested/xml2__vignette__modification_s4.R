# r2py crawler metadata
# package: xml2
# source_type: vignette
# topic: modification_s4
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xml2\doc\modification.R
# lines: 6

suppressPackageStartupMessages(library(xml2))
x <- read_xml("<a><b/></a>")
x
xml_name(x)
xml_name(x) <- "c"
x