# r2py crawler metadata
# package: xfun
# source_type: rd_example
# topic: attr2.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xfun\help
# lines: 5

suppressPackageStartupMessages(library(xfun))
z = structure(list(a = 1), foo = 2)
base::attr(z, "f")  # 2
xfun::attr2(z, "f")  # NULL
xfun::attr2(z, "foo")  # 2