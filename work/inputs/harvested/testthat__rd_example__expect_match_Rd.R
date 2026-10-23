# r2py crawler metadata
# package: testthat
# source_type: rd_example
# topic: expect_match.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\testthat\help
# lines: 10

suppressPackageStartupMessages(library(testthat))
expect_match("Testing is fun", "fun")
expect_match("Testing is fun", "f.n")
expect_no_match("Testing is fun", "horrible")

show_failure(expect_match("Testing is fun", "horrible"))
show_failure(expect_match("Testing is fun", "horrible", fixed = TRUE))

# Zero-length inputs always fail
show_failure(expect_match(character(), "."))