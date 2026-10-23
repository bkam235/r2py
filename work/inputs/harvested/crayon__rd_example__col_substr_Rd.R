# r2py crawler metadata
# package: crayon
# source_type: rd_example
# topic: col_substr.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\crayon\help
# lines: 23

suppressPackageStartupMessages(library(crayon))
str <- paste(
  red("red"),
  "default",
  green("green")
)

cat(str, "\n")
cat(col_substr(str, 1, 5), "\n")
cat(col_substr(str, 1, 15), "\n")
cat(col_substr(str, 3, 7), "\n")

substr(strip_style(str), 1, 5)
substr(strip_style(str), 1, 15)
substr(strip_style(str), 3, 7)

str2 <- "another " %+%
  red("multi-", sep = "", underline("style")) %+%
  " text"

cat(str2, "\n")
cat(col_substr(c(str, str2), c(3,5), c(7, 18)), sep = "\n")
substr(strip_style(c(str, str2)), c(3,5), c(7, 18))