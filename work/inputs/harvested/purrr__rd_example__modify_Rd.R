# r2py crawler metadata
# package: purrr
# source_type: rd_example
# topic: modify.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\purrr\help
# lines: 28

suppressPackageStartupMessages(library(purrr))
# Convert factors to characters
iris |>
  modify_if(is.factor, as.character) |>
  str()

# Specify which columns to map with a numeric vector of positions:
mtcars |> modify_at(c(1, 4, 5), as.character) |> str()

# Or with a vector of names:
mtcars |> modify_at(c("cyl", "am"), as.character) |> str()

list(x = sample(c(TRUE, FALSE), 100, replace = TRUE), y = 1:100) |>
  list_transpose(simplify = FALSE) |>
  modify_if("x", \(l) list(x = l$x, y = l$y * 100)) |>
  list_transpose()

# Use modify2() to map over two vectors and preserve the type of
# the first one:
x <- c(foo = 1L, bar = 2L)
y <- c(TRUE, FALSE)
modify2(x, y, \(x, cond) if (cond) x else 0L)

# Use a predicate function to decide whether to map a function:
modify_if(iris, is.factor, as.character)

# Specify an alternative with the `.else` argument:
modify_if(iris, is.factor, as.character, .else = as.integer)