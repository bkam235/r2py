# r2py crawler metadata
# package: purrr
# source_type: rd_example
# topic: lmap.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\purrr\help
# lines: 20

suppressPackageStartupMessages(library(purrr))
set.seed(1014)

# Let's write a function that returns a larger list or an empty list
# depending on some condition. It also uses the input name to name the
# output
maybe_rep <- function(x) {
  n <- rpois(1, 2)
  set_names(rep_len(x, n), paste0(names(x), seq_len(n)))
}

# The output size varies each time we map f()
x <- list(a = 1:4, b = letters[5:7], c = 8:9, d = letters[10])
x |> lmap(maybe_rep) |> str()

# We can apply f() on a selected subset of x
x |> lmap_at(c("a", "d"), maybe_rep) |> str()

# Or only where a condition is satisfied
x |> lmap_if(is.character, maybe_rep) |> str()