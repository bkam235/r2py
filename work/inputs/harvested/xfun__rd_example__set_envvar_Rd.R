# r2py crawler metadata
# package: xfun
# source_type: rd_example
# topic: set_envvar.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xfun\help
# lines: 5

suppressPackageStartupMessages(library(xfun))
vars = xfun::set_envvar(c(FOO = "1234"))
Sys.getenv("FOO")
xfun::set_envvar(vars)
Sys.getenv("FOO")