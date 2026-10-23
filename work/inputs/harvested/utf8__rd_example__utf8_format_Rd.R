# r2py crawler metadata
# package: utf8
# source_type: rd_example
# topic: utf8_format.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\utf8\help
# lines: 9

suppressPackageStartupMessages(library(utf8))
# the second element is encoded in latin-1, but declared as UTF-8
x <- c("fa\u00E7ile", "fa\xE7ile", "fa\xC3\xA7ile")
Encoding(x) <- c("UTF-8", "UTF-8", "bytes")

# formatting
utf8_format(x, chars = 3)
utf8_format(x, chars = 3, justify = "centre", width = 10)
utf8_format(x, chars = 3, justify = "right")