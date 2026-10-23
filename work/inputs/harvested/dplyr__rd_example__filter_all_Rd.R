# r2py crawler metadata
# package: dplyr
# source_type: rd_example
# topic: filter_all.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\help
# lines: 31

suppressPackageStartupMessages(library(dplyr))
# While filter() accepts expressions with specific variables, the
# scoped filter verbs take an expression with the pronoun `.` and
# replicate it over all variables. This expression should be quoted
# with all_vars() or any_vars():
all_vars(is.na(.))
any_vars(is.na(.))


# You can take the intersection of the replicated expressions:
filter_all(mtcars, all_vars(. > 150))
# ->
filter(mtcars, if_all(everything(), ~ .x > 150))

# Or the union:
filter_all(mtcars, any_vars(. > 150))
# ->
filter(mtcars, if_any(everything(), ~ . > 150))


# You can vary the selection of columns on which to apply the
# predicate. filter_at() takes a vars() specification:
filter_at(mtcars, vars(starts_with("d")), any_vars((. %% 2) == 0))
# ->
filter(mtcars, if_any(starts_with("d"), ~ (.x %% 2) == 0))

# And filter_if() selects variables with a predicate function:
filter_if(mtcars, ~ all(floor(.) == .), all_vars(. != 0))
# ->
is_int <- function(x) all(floor(x) == x)
filter(mtcars, if_all(where(is_int), ~ .x != 0))