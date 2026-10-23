# r2py crawler metadata
# package: testthat
# source_type: rd_example
# topic: expect_setequal.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\testthat\help
# lines: 9

suppressPackageStartupMessages(library(testthat))
expect_setequal(letters, rev(letters))
show_failure(expect_setequal(letters[-1], rev(letters)))

x <- list(b = 2, a = 1)
expect_mapequal(x, list(a = 1, b = 2))
show_failure(expect_mapequal(x, list(a = 1)))
show_failure(expect_mapequal(x, list(a = 1, b = "x")))
show_failure(expect_mapequal(x, list(a = 1, b = 2, c = 3)))