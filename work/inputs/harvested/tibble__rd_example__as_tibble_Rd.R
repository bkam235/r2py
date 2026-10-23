# r2py crawler metadata
# package: tibble
# source_type: rd_example
# topic: as_tibble.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\tibble\help
# lines: 14

suppressPackageStartupMessages(library(tibble))
m <- matrix(rnorm(50), ncol = 5)
colnames(m) <- c("a", "b", "c", "d", "e")
df <- as_tibble(m)

as_tibble_row(c(a = 1, b = 2))
as_tibble_row(list(c = "three", d = list(4:5)))
as_tibble_row(1:3, .name_repair = "unique")

as_tibble_col(1:3)
as_tibble_col(
  list(c = "three", d = list(4:5)),
  column_name = "data"
)