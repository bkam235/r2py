# r2py crawler metadata
# package: dplyr
# source_type: rd_example
# topic: mutate_all.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\help
# lines: 53

suppressPackageStartupMessages(library(dplyr))
iris <- as_tibble(iris)

# All variants can be passed functions and additional arguments,
# purrr-style. The _at() variants directly support strings. Here
# we'll scale the variables `height` and `mass`:
scale2 <- function(x, na.rm = FALSE) (x - mean(x, na.rm = na.rm)) / sd(x, na.rm)
starwars |> mutate_at(c("height", "mass"), scale2)
# ->
starwars |> mutate(across(c("height", "mass"), scale2))

# You can pass additional arguments to the function:
starwars |> mutate_at(c("height", "mass"), scale2, na.rm = TRUE)
starwars |> mutate_at(c("height", "mass"), ~scale2(., na.rm = TRUE))
# ->
starwars |> mutate(across(c("height", "mass"), ~ scale2(.x, na.rm = TRUE)))

# You can also supply selection helpers to _at() functions but you have
# to quote them with vars():
iris |> mutate_at(vars(matches("Sepal")), log)
iris |> mutate(across(matches("Sepal"), log))

# The _if() variants apply a predicate function (a function that
# returns TRUE or FALSE) to determine the relevant subset of
# columns. Here we divide all the numeric columns by 100:
starwars |> mutate_if(is.numeric, scale2, na.rm = TRUE)
starwars |> mutate(across(where(is.numeric), ~ scale2(.x, na.rm = TRUE)))

# mutate_if() is particularly useful for transforming variables from
# one type to another
iris |> mutate_if(is.factor, as.character)
iris |> mutate_if(is.double, as.integer)
# ->
iris |> mutate(across(where(is.factor), as.character))
iris |> mutate(across(where(is.double), as.integer))

# Multiple transformations ----------------------------------------

# If you want to apply multiple transformations, pass a list of
# functions. When there are multiple functions, they create new
# variables instead of modifying the variables in place:
iris |> mutate_if(is.numeric, list(scale2, log))
iris |> mutate_if(is.numeric, list(~scale2(.), ~log(.)))
iris |> mutate_if(is.numeric, list(scale = scale2, log = log))
# ->
iris |>
  as_tibble() |>
  mutate(across(where(is.numeric), list(scale = scale2, log = log)))

# When there's only one function in the list, it modifies existing
# variables in place. Give it a name to instead create new variables:
iris |> mutate_if(is.numeric, list(scale2))
iris |> mutate_if(is.numeric, list(scale = scale2))