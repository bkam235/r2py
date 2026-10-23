# r2py crawler metadata
# package: vctrs
# source_type: rd_example
# topic: vec_detect_complete.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\vctrs\help
# lines: 19

suppressPackageStartupMessages(library(vctrs))
x <- c(1, 2, NA, 4, NA)

# For most vectors, this is identical to `!vec_detect_missing(x)`
vec_detect_complete(x)
!vec_detect_missing(x)

df <- data_frame(
  x = x,
  y = c("a", "b", NA, "d", "e")
)

# This returns `TRUE` where all elements of the row are non-missing.
# Compare that with `!vec_detect_missing()`, which detects rows that have at
# least one non-missing value.
df2 <- df
df2$all_non_missing <- vec_detect_complete(df)
df2$any_non_missing <- !vec_detect_missing(df)
df2