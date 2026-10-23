# r2py crawler metadata
# package: data.table
# source_type: rd_example
# topic: test.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\data.table\help
# lines: 13

suppressPackageStartupMessages(library(data.table))
test = data.table:::test
test(1, x = sum(1:5), y = 15L)
test(2, log(-1), NaN, warning="NaNs")
test(3, sum("a"), error="invalid.*character")
# test failure example
stopifnot(
  test(4, TRUE, FALSE) == FALSE
)
# NA_real_ vs NaN
test(5.01, NA_real_, NaN)
test(5.03, all.equal(NaN, NA_real_))
test(5.02, identical(NaN, NA_real_), FALSE)