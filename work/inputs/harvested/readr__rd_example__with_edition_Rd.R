# r2py crawler metadata
# package: readr
# source_type: rd_example
# topic: with_edition.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\readr\help
# lines: 17

suppressPackageStartupMessages(library(readr))
with_edition(1, edition_get())
with_edition(2, edition_get())

# readr 1e and 2e behave differently when input rows have different number
# number of fields
with_edition(1, read_csv("1,2\n3,4,5", col_names = c("X", "Y", "Z")))
with_edition(2, read_csv("1,2\n3,4,5", col_names = c("X", "Y", "Z")))

# local_edition() applies in a specific scope, for example, inside a function
read_csv_1e <- function(...) {
  local_edition(1)
  read_csv(...)
}
read_csv("1,2\n3,4,5", col_names = c("X", "Y", "Z"))      # 2e behaviour
read_csv_1e("1,2\n3,4,5", col_names = c("X", "Y", "Z"))   # 1e behaviour
read_csv("1,2\n3,4,5", col_names = c("X", "Y", "Z"))      # 2e behaviour