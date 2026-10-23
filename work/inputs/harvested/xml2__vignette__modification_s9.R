# r2py crawler metadata
# package: xml2
# source_type: vignette
# topic: modification_s9
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xml2\doc\modification.R
# lines: 7

suppressPackageStartupMessages(library(xml2))
x <- read_xml("<a><b /><b><b /></b></a>")
bees <- xml_find_all(x, "//b")
xml_remove(xml_child(x), free = TRUE)
# bees[[1]] is no longer valid!!!
rm(bees)
gc()