# r2py crawler metadata
# package: xml2
# source_type: rd_example
# topic: xml_serialize.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xml2\help
# lines: 9

library(xml2)
x <- read_xml("<a>
  <b><c>123</c></b>
  <b><c>456</c></b>
</a>")

b <- xml_find_all(x, "//b")
out <- xml_serialize(b, NULL)
xml_unserialize(out)