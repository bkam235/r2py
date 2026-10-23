# r2py crawler metadata
# package: htmltools
# source_type: rd_example
# topic: tagAppendAttributes.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\htmltools\help
# lines: 8

suppressPackageStartupMessages(library(htmltools))
html <- div(a())
tagAppendAttributes(html, class = "foo")
tagAppendAttributes(html, .cssSelector = "a", class = "bar")
tagAppendAttributes(html, contenteditable = NA)

tagHasAttribute(div(foo = "bar"), "foo")
tagGetAttribute(div(foo = "bar"), "foo")