# r2py crawler metadata
# package: rlang
# source_type: rd_example
# topic: dyn-dots.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rlang\help
# lines: 19

suppressPackageStartupMessages(library(rlang))
f <- function(...) {
  out <- list2(...)
  rev(out)
}

# Trailing commas are ignored
f(this = "that", )

# Splice lists of arguments with `!!!`
x <- list(alpha = "first", omega = "last")
f(!!!x)

# Inject a name using glue syntax
if (is_installed("glue")) {
  nm <- "key"
  f("{nm}" := "value")
  f("prefix_{nm}" := "value")
}