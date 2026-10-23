# r2py crawler metadata
# package: cli
# source_type: rd_example
# topic: ansi_substring.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\cli\help
# lines: 25

suppressPackageStartupMessages(library(cli))
str <- paste(
  col_red("red"),
  "default",
  col_green("green")
)

cat(str, "\n")
cat(ansi_substring(str, 1, 5), "\n")
cat(ansi_substring(str, 1, 15), "\n")
cat(ansi_substring(str, 3, 7), "\n")

substring(ansi_strip(str), 1, 5)
substring(ansi_strip(str), 1, 15)
substring(ansi_strip(str), 3, 7)

str2 <- paste(
  "another",
  col_red("multi-", style_underline("style")),
  "text"
)

cat(str2, "\n")
cat(ansi_substring(str2, c(3,5), c(7, 18)), sep = "\n")
substring(ansi_strip(str2), c(3,5), c(7, 18))