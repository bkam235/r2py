# r2py crawler metadata
# package: crayon
# source_type: rd_example
# topic: col_substring.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\crayon\help
# lines: 23

suppressPackageStartupMessages(library(crayon))
str <- paste(
  red("red"),
  "default",
  green("green")
)

cat(str, "\n")
cat(col_substring(str, 1, 5), "\n")
cat(col_substring(str, 1, 15), "\n")
cat(col_substring(str, 3, 7), "\n")

substring(strip_style(str), 1, 5)
substring(strip_style(str), 1, 15)
substring(strip_style(str), 3, 7)

str2 <- "another " %+%
  red("multi-", sep = "", underline("style")) %+%
  " text"

cat(str2, "\n")
cat(col_substring(str2, c(3,5), c(7, 18)), sep = "\n")
substring(strip_style(str2), c(3,5), c(7, 18))