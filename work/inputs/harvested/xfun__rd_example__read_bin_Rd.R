# r2py crawler metadata
# package: xfun
# source_type: rd_example
# topic: read_bin.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xfun\help
# lines: 5

suppressPackageStartupMessages(library(xfun))
f = tempfile()
cat("abc", file = f)
xfun::read_bin(f)
unlink(f)