# r2py crawler metadata
# package: htmltools
# source_type: rd_example
# topic: tagAppendChild.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\htmltools\help
# lines: 11

suppressPackageStartupMessages(library(htmltools))
html <- div(a(), h1())
tagAppendChild(html, span())
tagAppendChild(html, .cssSelector = "a", span())

tagAppendChildren(html, span(), p())
tagAppendChildren(html, .cssSelector = "a", span(), p())

tagSetChildren(html, span(), p())

tagInsertChildren(html, after = 1, span(), p())