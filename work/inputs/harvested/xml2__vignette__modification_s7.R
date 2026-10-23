# r2py crawler metadata
# package: xml2
# source_type: vignette
# topic: modification_s7
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xml2\doc\modification.R
# lines: 12

suppressPackageStartupMessages(library(xml2))
x <- read_xml("<parent><child>1</child><child>2<child>3</child></child></parent>")
children <- xml_children(x)
t1 <- children[[1]]
t2 <- children[[2]]
t3 <- xml_children(children[[2]])[[1]]

xml_add_child(t1, t3)
x

xml_add_child(t1, read_xml("<test/>"))
x