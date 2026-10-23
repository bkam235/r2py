# r2py crawler metadata
# package: xfun
# source_type: rd_example
# topic: is_sub_path.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xfun\help
# lines: 4

suppressPackageStartupMessages(library(xfun))
xfun::is_sub_path("a/b/c.txt", "a/b")  # TRUE
xfun::is_sub_path("a/b/c.txt", "d/b")  # FALSE
xfun::is_sub_path("a/b/c.txt", "a\\b")  # FALSE (even on Windows)