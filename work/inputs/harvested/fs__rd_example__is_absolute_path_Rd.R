# r2py crawler metadata
# package: fs
# source_type: rd_example
# topic: is_absolute_path.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\fs\help
# lines: 6

suppressPackageStartupMessages(library(fs))
is_absolute_path("/foo")
is_absolute_path("C:\\foo")
is_absolute_path("\\\\myserver\\foo\\bar")

is_absolute_path("foo/bar")