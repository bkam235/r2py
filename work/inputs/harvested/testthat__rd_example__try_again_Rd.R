# r2py crawler metadata
# package: testthat
# source_type: rd_example
# topic: try_again.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\testthat\help
# lines: 14

suppressPackageStartupMessages(library(testthat))
usually_return_1 <- function(i) {
  if (runif(1) < 0.1) 0 else 1
}


# 10% chance of failure:
expect_equal(usually_return_1(), 1)

# 1% chance of failure:
try_again(1, expect_equal(usually_return_1(), 1))

# 0.1% chance of failure:
try_again(2, expect_equal(usually_return_1(), 1))