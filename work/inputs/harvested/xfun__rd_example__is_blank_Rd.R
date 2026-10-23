# r2py crawler metadata
# package: xfun
# source_type: rd_example
# topic: is_blank.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xfun\help
# lines: 5

suppressPackageStartupMessages(library(xfun))
xfun::is_blank("")
xfun::is_blank("abc")
xfun::is_blank(c("", "  ", "\n\t"))
xfun::is_blank(c("", " ", "abc"))