# r2py crawler metadata
# package: purrr
# source_type: rd_example
# topic: modify_tree.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\purrr\help
# lines: 17

suppressPackageStartupMessages(library(purrr))
x <- list(list(a = 2:1, c = list(b1 = 2), b = list(c2 = 3, c1 = 4)))
x |> str()

# Transform each leaf
x |> modify_tree(leaf = \(x) x + 100) |>  str()

# Recursively sort the nodes
sort_named <- function(x) {
  nms <- names(x)
  if (!is.null(nms)) {
    x[order(nms)]
  } else {
    x
   }
}
x |> modify_tree(post = sort_named) |> str()