# r2py crawler metadata
# package: xfun
# source_type: rd_example
# topic: alnum_id.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xfun\help
# lines: 6

suppressPackageStartupMessages(library(xfun))
x = c("Hello world 123!", "a  &b*^##c 456")
xfun::alnum_id(x)
xfun::alnum_id(x, "[^[:alpha:]]+")  # only keep alphabetical chars
# when text contains HTML tags
xfun::alnum_id("<h1>Hello <strong>world</strong>!")