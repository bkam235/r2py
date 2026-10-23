# r2py crawler metadata
# package: sass
# source_type: rd_example
# topic: sass_import.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\sass\help
# lines: 8

suppressPackageStartupMessages(library(sass))
sass_import("foo")
sass_import("$foo", FALSE)

tmp_scss_file <- tempfile(fileext = ".scss")
writeLines("$color: red; body{ color: $color; }", tmp_scss_file)
sass_file(tmp_scss_file)
sass(sass_file(tmp_scss_file))