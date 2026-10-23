# r2py crawler metadata
# package: xml2
# source_type: rd_example
# topic: xml_ns_strip.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xml2\help
# lines: 16

suppressPackageStartupMessages(library(xml2))
x <- read_xml(
  "<foo xmlns = 'http://foo.com'>
   <baz/>
   <bar xmlns = 'http://bar.com'>
     <baz/>
   </bar>
  </foo>"
)
# Need to specify the default namespaces to find the baz nodes
xml_find_all(x, "//d1:baz")
xml_find_all(x, "//d2:baz")

# After stripping the default namespaces you can find both baz nodes directly
xml_ns_strip(x)
xml_find_all(x, "//baz")