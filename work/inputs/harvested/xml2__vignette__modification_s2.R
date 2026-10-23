# r2py crawler metadata
# package: xml2
# source_type: vignette
# topic: modification_s2
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xml2\doc\modification.R
# lines: 14

suppressPackageStartupMessages(library(xml2))
x <- read_xml("<p>This is some <b>text</b>. This is more.</p>")
xml_text(x)

xml_text(x) <- "This is some other text."
xml_text(x)

# You can avoid this by explicitly selecting the text node.
x <- read_xml("<p>This is some text. This is <b>bold!</b></p>")
text_only <- xml_find_all(x, "//text()")

xml_text(text_only) <- c("This is some other text. ", "Still bold!")
xml_text(x)
xml_structure(x)