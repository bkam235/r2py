# r2py crawler metadata
# package: tibble
# source_type: rd_example
# topic: formatting.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\tibble\help
# lines: 16

suppressPackageStartupMessages(library(tibble))
print(as_tibble(mtcars))
print(as_tibble(mtcars), n = 1)
print(as_tibble(mtcars), n = 3)

print(as_tibble(trees), n = 100)

print(mtcars, width = 10)

mtcars2 <- as_tibble(cbind(mtcars, mtcars), .name_repair = "unique")
print(mtcars2, n = 25, max_extra_cols = 3)

if (requireNamespace("nycflights13", quietly = TRUE)) withAutoprint({ # examplesIf
print(nycflights13::flights, max_footer_lines = 1)
print(nycflights13::flights, width = Inf)
}) # examplesIf