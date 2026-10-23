# r2py crawler metadata
# package: dplyr
# source_type: rd_example
# topic: group_by_all.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\help
# lines: 26

suppressPackageStartupMessages(library(dplyr))
# Group a data frame by all variables:
group_by_all(mtcars)
# ->
mtcars |> group_by(pick(everything()))

# Group by variables selected with a predicate:
group_by_if(iris, is.factor)
# ->
iris |> group_by(pick(where(is.factor)))

# Group by variables selected by name:
group_by_at(mtcars, vars(vs, am))
# ->
mtcars |> group_by(pick(vs, am))

# Like group_by(), the scoped variants have optional mutate
# semantics. This provide a shortcut for group_by() + mutate():
d <- tibble(x=c(1,1,2,2), y=c(1,2,1,2))
group_by_all(d, as.factor)
# ->
d |> group_by(across(everything(), as.factor))

group_by_if(iris, is.factor, as.character)
# ->
iris |> group_by(across(where(is.factor), as.character))