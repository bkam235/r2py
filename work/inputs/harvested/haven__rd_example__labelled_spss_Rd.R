# r2py crawler metadata
# package: haven
# source_type: rd_example
# topic: labelled_spss.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\haven\help
# lines: 14

suppressPackageStartupMessages(library(haven))
x1 <- labelled_spss(1:10, c(Good = 1, Bad = 8), na_values = c(9, 10))
is.na(x1)

x2 <- labelled_spss(
  1:10,
  c(Good = 1, Bad = 8),
  na_range = c(9, Inf),
  label = "Quality rating"
)
is.na(x2)

# Print data and metadata
x2