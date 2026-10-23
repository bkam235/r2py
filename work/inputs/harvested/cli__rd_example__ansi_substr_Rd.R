# r2py crawler metadata
# package: cli
# source_type: rd_example
# topic: ansi_substr.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\cli\help
# lines: 25

suppressPackageStartupMessages(library(cli))
str <- paste(
  col_red("red"),
  "default",
  col_green("green")
)

cat(str, "\n")
cat(ansi_substr(str, 1, 5), "\n")
cat(ansi_substr(str, 1, 15), "\n")
cat(ansi_substr(str, 3, 7), "\n")

substr(ansi_strip(str), 1, 5)
substr(ansi_strip(str), 1, 15)
substr(ansi_strip(str), 3, 7)

str2 <- paste(
  "another",
  col_red("multi-", style_underline("style")),
  "text"
)

cat(str2, "\n")
cat(ansi_substr(c(str, str2), c(3,5), c(7, 18)), sep = "\n")
substr(ansi_strip(c(str, str2)), c(3,5), c(7, 18))