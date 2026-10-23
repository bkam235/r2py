# r2py crawler metadata
# package: purrr
# source_type: rd_example
# topic: every.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\purrr\help
# lines: 13

suppressPackageStartupMessages(library(purrr))
x <- list(0:10, 5.5)
x |> every(is.numeric)
x |> every(is.integer)
x |> some(is.integer)
x |> none(is.character)

# Missing values are propagated:
some(list(NA, FALSE), identity)

# If you need to use these functions in a context where missing values are
# unsafe (e.g. in `if ()` conditions), make sure to use safe predicates:
if (some(list(NA, FALSE), rlang::is_true)) "foo" else "bar"