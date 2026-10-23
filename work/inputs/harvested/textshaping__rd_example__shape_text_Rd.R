# r2py crawler metadata
# package: textshaping
# source_type: rd_example
# topic: shape_text.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\textshaping\help
# lines: 14

suppressPackageStartupMessages(library(textshaping))
string <- "This is a long string\nLook; It spans multiple lines\nand all"

# Shape with default settings
shape_text(string)

# Mix styles within the same string
string <- c(
  "This string will have\na ",
  "very large",
  " text style\nin the middle"
)

shape_text(string, id = c(1, 1, 1), size = c(12, 24, 12))