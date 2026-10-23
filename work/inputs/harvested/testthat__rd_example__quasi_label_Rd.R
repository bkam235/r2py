# r2py crawler metadata
# package: testthat
# source_type: rd_example
# topic: quasi_label.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\testthat\help
# lines: 13

suppressPackageStartupMessages(library(testthat))
f <- function(i) if (i > 3) i * 9 else i * 10
i <- 10

# This sort of expression commonly occurs inside a for loop or function
# And the failure isn't helpful because you can't see the value of i
# that caused the problem:
show_failure(expect_equal(f(i), i * 10))

# To overcome this issue, testthat allows you to unquote expressions using
# !!. This causes the failure message to show the value rather than the
# variable name
show_failure(expect_equal(f(!!i), !!(i * 10)))