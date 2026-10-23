# r2py crawler metadata
# package: evaluate
# source_type: rd_example
# topic: parse_all.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\evaluate\help
# lines: 28

suppressPackageStartupMessages(library(evaluate))
# Each of these inputs are single line, but generate different numbers of
# expressions
source <- c(
  "# a comment",
  "x",
  "x;y",
  "x;y;z"
)
parsed <- parse_all(source)
lengths(parsed$expr)
str(parsed$expr)

# Each of these inputs are a single expression, but span different numbers
# of lines
source <- c(
  "function() {}",
  "function() {",
  "  # Hello!",
  "}",
  "function() {",
  "  # Hello!",
  "  # Goodbye!",
  "}"
)
parsed <- parse_all(source)
lengths(parsed$expr)
parsed$src