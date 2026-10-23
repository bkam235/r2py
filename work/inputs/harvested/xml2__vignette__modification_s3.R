# r2py crawler metadata
# package: xml2
# source_type: vignette
# topic: modification_s3
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xml2\doc\modification.R
# lines: 20

suppressPackageStartupMessages(library(xml2))
x <- read_xml("<a href='invalid!'>xml2</a>")
xml_attr(x, "href")

xml_attr(x, "href") <- "https://github.com/r-lib/xml2"
xml_attr(x, "href")

xml_attrs(x) <- c(id = "xml2", href = "https://github.com/r-lib/xml2")
xml_attrs(x)
x

xml_attrs(x) <- NULL
x

# Namespaces are added with as a xmlns or xmlns:prefix attribute
xml_attr(x, "xmlns") <- "http://foo"
x

xml_attr(x, "xmlns:bar") <- "http://bar"
x