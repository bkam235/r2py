# r2py crawler metadata
# package: xml2
# source_type: vignette
# topic: modification_s8
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xml2\doc\modification.R
# lines: 14

suppressPackageStartupMessages(library(xml2))
x <- read_xml("<foo><bar><baz/></bar></foo>")
x1 <- x |>
  xml_children() |>
  (\(.) .[[1]])()
x2 <- x1 |>
  xml_children() |>
  (\(.) .[[1]])()

xml_remove(x1)
rm(x1)
gc()

x2