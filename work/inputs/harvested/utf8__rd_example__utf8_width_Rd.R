# r2py crawler metadata
# package: utf8
# source_type: rd_example
# topic: utf8_width.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\utf8\help
# lines: 10

suppressPackageStartupMessages(library(utf8))
# the second element is encoded in latin-1, but declared as UTF-8
x <- c("fa\u00E7ile", "fa\xE7ile", "fa\xC3\xA7ile")
Encoding(x) <- c("UTF-8", "UTF-8", "bytes")

# get widths
utf8_width(x)
utf8_width(x, encode = FALSE)
utf8_width('"')
utf8_width('"', quote = TRUE)