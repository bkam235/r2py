# r2py crawler metadata
# package: xml2
# source_type: vignette
# topic: modification_s10
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xml2\doc\modification.R
# lines: 12

suppressPackageStartupMessages(library(xml2))
d <- xml_new_root("sld",
  "xmlns" = "http://www.opengis.net/sld",
  "xmlns:ogc" = "http://www.opengis.net/ogc",
  "xmlns:se" = "http://www.opengis.net//se",
  version = "1.1.0"
) |>
  xml_add_child("layer") |>
  xml_add_child("se:Name", "My Layer") |>
  xml_root()

d