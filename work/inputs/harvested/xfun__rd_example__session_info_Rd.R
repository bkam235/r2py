# r2py crawler metadata
# package: xfun
# source_type: rd_example
# topic: session_info.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xfun\help
# lines: 5

suppressPackageStartupMessages(library(xfun))
if (interactive()) {
xfun::session_info()
if (xfun::loadable("MASS")) xfun::session_info("MASS")
}