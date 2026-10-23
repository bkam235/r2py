# r2py crawler metadata
# package: testthat
# source_type: rd_example
# topic: expect_vector.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\testthat\help
# lines: 6

suppressPackageStartupMessages(library(testthat))
if (requireNamespace("vctrs")) withAutoprint({ # examplesIf
expect_vector(1:10, ptype = integer(), size = 10)
show_failure(expect_vector(1:10, ptype = integer(), size = 5))
show_failure(expect_vector(1:10, ptype = character(), size = 5))
}) # examplesIf