# r2py crawler metadata
# package: xml2
# source_type: rd_example
# topic: xml_dtd.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xml2\help
# lines: 17

suppressPackageStartupMessages(library(xml2))
r <- xml_new_root(
  xml_dtd(
    "html",
    "-//W3C//DTD XHTML 1.0 Transitional//EN",
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"
  )
)

# Use read_xml directly for more complicated DTD
d <- read_xml(
  '<!DOCTYPE doc [
<!ELEMENT doc (#PCDATA)>
<!ENTITY foo " test ">
]>
<doc>This is a valid document &foo; !</doc>'
)