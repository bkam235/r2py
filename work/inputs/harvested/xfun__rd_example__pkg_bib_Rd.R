# r2py crawler metadata
# package: xfun
# source_type: rd_example
# topic: pkg_bib.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xfun\help
# lines: 4

suppressPackageStartupMessages(library(xfun))
pkg_bib(c("base", "MASS", "xfun"))
pkg_bib("cluster", prefix = "R-pkg-")  # a different prefix
pkg_bib("xfun", date = "package")