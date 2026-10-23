# r2py crawler metadata
# package: xfun
# source_type: rd_example
# topic: valid_syntax.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xfun\help
# lines: 4

suppressPackageStartupMessages(library(xfun))
xfun::valid_syntax("1+1")
xfun::valid_syntax("1+")
xfun::valid_syntax(c("if(T){1+1}", "else {2+2}"), silent = FALSE)