# r2py crawler metadata
# package: testthat
# source_type: rd_example
# topic: Reporter.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\testthat\help
# lines: 6

suppressPackageStartupMessages(library(testthat))
path <- testthat_example("success")

test_file(path)
# Override the default by supplying the name of a reporter
test_file(path, reporter = "minimal")