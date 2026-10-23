# r2py crawler metadata
# package: haven
# source_type: rd_example
# topic: zap_missing.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\haven\help
# lines: 20

suppressPackageStartupMessages(library(haven))
x1 <- labelled(
  c(1, 5, tagged_na("a", "b")),
  c(Unknown = tagged_na("a"), Refused = tagged_na("b"))
)
x1
zap_missing(x1)

x2 <- labelled_spss(
  c(1, 2, 1, 99),
  c(missing = 99),
  na_value = 99
)
x2
zap_missing(x2)

# You can also apply to data frames
df <- tibble::tibble(x1, x2, y = 4:1)
df
zap_missing(df)