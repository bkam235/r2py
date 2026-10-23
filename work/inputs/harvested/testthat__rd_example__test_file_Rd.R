# r2py crawler metadata
# package: testthat
# source_type: rd_example
# topic: test_file.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\testthat\help
# lines: 5

suppressPackageStartupMessages(library(testthat))
path <- testthat_example("success")
test_file(path)
test_file(path, desc = "some tests have warnings")
test_file(path, reporter = "minimal")