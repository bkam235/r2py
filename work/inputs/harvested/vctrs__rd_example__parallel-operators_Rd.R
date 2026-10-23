# r2py crawler metadata
# package: vctrs
# source_type: rd_example
# topic: parallel-operators.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\vctrs\help
# lines: 40

suppressPackageStartupMessages(library(vctrs))
a <- c(TRUE, TRUE, TRUE, FALSE, FALSE, FALSE, NA, NA, NA)
b <- c(TRUE, FALSE, NA, TRUE, FALSE, NA, TRUE, FALSE, NA)

# Default behavior treats missings like `|` does
vec_pany(a, b)
a | b

# Default behavior treats missings like `&` does
vec_pall(a, b)
a & b

# Remove missings from the computation, like `na_rm = TRUE`
vec_pany(a, b, .missing = FALSE)
(a & !is.na(a)) | (b & !is.na(b))

vec_pall(a, b, .missing = TRUE)
(a | is.na(a)) & (b | is.na(b))

# `vec_pall()` can be used to implement a `dplyr::filter()` style API
df <- data_frame(id = seq_along(a), a = a, b = b)

keep_rows <- function(x, ...) {
  vec_slice(x, vec_pall(..., .missing = FALSE))
}
drop_rows <- function(x, ...) {
  vec_slice(x, !vec_pall(..., .missing = FALSE))
}

# "Keep / Drop the rows when both a and b are TRUE"
# These form complements of one another, even with `NA`s.
keep_rows(df, a, b)
drop_rows(df, a, b)

# Same empty behavior as `any()` and `all()`
vec_pany(.size = 1)
any()

vec_pall(.size = 1)
all()