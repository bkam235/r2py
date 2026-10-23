# r2py crawler metadata
# package: xfun
# source_type: rd_example
# topic: relative_path.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xfun\help
# lines: 4

suppressPackageStartupMessages(library(xfun))
xfun::relative_path("foo/bar.txt", "foo/")
xfun::relative_path("foo/bar/a.txt", "foo/haha/")
xfun::relative_path(getwd())