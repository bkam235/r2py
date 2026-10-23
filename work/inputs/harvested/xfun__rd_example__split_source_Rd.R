# r2py crawler metadata
# package: xfun
# source_type: rd_example
# topic: split_source.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xfun\help
# lines: 4

suppressPackageStartupMessages(library(xfun))
code = c("# comment 1", "# comment 2", "if (TRUE) {", "1 + 1", "}", "print(1:5)")
xfun::split_source(code)
xfun::split_source(code, merge_comments = TRUE)