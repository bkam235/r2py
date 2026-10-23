# r2py crawler metadata
# package: dplyr
# source_type: rd_example
# topic: all_equal.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\help
# lines: 13

suppressPackageStartupMessages(library(dplyr))
scramble <- function(x) x[sample(nrow(x)), sample(ncol(x))]

# `all_equal()` ignored row and column ordering by default,
# but we now feel that that makes it too easy to make mistakes
mtcars2 <- scramble(mtcars)
all_equal(mtcars, mtcars2)

# Instead, be explicit about the row and column ordering
all.equal(
  mtcars,
  mtcars2[rownames(mtcars), names(mtcars)]
)