# r2py crawler metadata
# package: xml2
# source_type: rd_example
# topic: xml_find_all.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xml2\help
# lines: 46

suppressPackageStartupMessages(library(xml2))
x <- read_xml("<foo><bar><baz/></bar><baz/></foo>")
xml_find_all(x, ".//baz")
xml_path(xml_find_all(x, ".//baz"))

# Note the difference between .// and //
# //  finds anywhere in the document (ignoring the current node)
# .// finds anywhere beneath the current node
(bar <- xml_find_all(x, ".//bar"))
xml_find_all(bar, ".//baz")
xml_find_all(bar, "//baz")

# Find all vs find one -----------------------------------------------------
x <- read_xml("<body>
  <p>Some <b>text</b>.</p>
  <p>Some <b>other</b> <b>text</b>.</p>
  <p>No bold here!</p>
</body>")
para <- xml_find_all(x, ".//p")

# By default, if you apply xml_find_all to a nodeset, it finds all matches,
# de-duplicates them, and returns as a single nodeset. This means you
# never know how many results you'll get
xml_find_all(para, ".//b")

# If you set flatten to FALSE, though, xml_find_all will return a list of
# nodesets, where each nodeset contains the matches for the corresponding
# node in the original nodeset.
xml_find_all(para, ".//b", flatten = FALSE)

# xml_find_first only returns the first match per input node. If there are 0
# matches it will return a missing node
xml_find_first(para, ".//b")
xml_text(xml_find_first(para, ".//b"))

# Namespaces ---------------------------------------------------------------
# If the document uses namespaces, you'll need use xml_ns to form
# a unique mapping between full namespace url and a short prefix
x <- read_xml('
 <root xmlns:f = "http://foo.com" xmlns:g = "http://bar.com">
   <f:doc><g:baz /></f:doc>
   <f:doc><g:baz /></f:doc>
 </root>
')
xml_find_all(x, ".//f:doc")
xml_find_all(x, ".//f:doc", xml_ns(x))