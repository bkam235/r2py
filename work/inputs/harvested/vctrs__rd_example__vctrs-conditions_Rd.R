# r2py crawler metadata
# package: vctrs
# source_type: rd_example
# topic: vctrs-conditions.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\vctrs\help
# lines: 32

suppressPackageStartupMessages(library(vctrs))
# Most of the time, `maybe_lossy_cast()` returns its input normally:
maybe_lossy_cast(
  c("foo", "bar"),
  NA,
  "",
  lossy = c(FALSE, FALSE),
  x_arg = "",
  to_arg = ""
)

# If `lossy` has any `TRUE`, an error is thrown:
try(maybe_lossy_cast(
  c("foo", "bar"),
  NA,
  "",
  lossy = c(FALSE, TRUE),
  x_arg = "",
  to_arg = ""
))

# Unless lossy casts are allowed:
allow_lossy_cast(
  maybe_lossy_cast(
    c("foo", "bar"),
    NA,
    "",
    lossy = c(FALSE, TRUE),
    x_arg = "",
    to_arg = ""
  )
)