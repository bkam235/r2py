# r2py crawler metadata
# package: purrr
# source_type: rd_example
# topic: accumulate.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\purrr\help
# lines: 77

suppressPackageStartupMessages(library(purrr))
# With an associative operation, the final value is always the
# same, no matter the direction. You'll find it in the first element for a
# backward (left) accumulation, and in the last element for forward
# (right) one:
1:5 |> accumulate(`+`)
1:5 |> accumulate(`+`, .dir = "backward")

# The final value is always equal to the equivalent reduction:
1:5 |> reduce(`+`)

# It is easier to understand the details of the reduction with
# `paste()`.
accumulate(letters[1:5], paste, sep = ".")

# Note how the intermediary reduced values are passed to the left
# with a left reduction, and to the right otherwise:
accumulate(letters[1:5], paste, sep = ".", .dir = "backward")

# By ignoring the input vector (nxt), you can turn output of one step into
# the input for the next. This code takes 10 steps of a random walk:
accumulate(1:10, \(acc, nxt) acc + rnorm(1), .init = 0)

# `accumulate2()` is a version of `accumulate()` that works with
# 3-argument functions and one additional vector:
paste2 <- function(acc, nxt, sep = ".") paste(acc, nxt, sep = sep)
letters[1:4] |> accumulate(paste2)
letters[1:4] |> accumulate2(c("-", ".", "-"), paste2)

# You can shortcircuit an accumulation and terminate it early by
# returning a value wrapped in a done(). In the following example
# we return early if the result-so-far, which is passed on the LHS,
# meets a condition:
paste3 <- function(out, input, sep = ".") {
  if (nchar(out) > 4) {
    return(done(out))
  }
  paste(out, input, sep = sep)
}
letters |> accumulate(paste3)

# Note how we get twice the same value in the accumulation. That's
# because we have returned it twice. To prevent this, return an empty
# done box to signal to accumulate() that it should terminate with the
# value of the last iteration:
paste3 <- function(out, input, sep = ".") {
  if (nchar(out) > 4) {
    return(done())
  }
  paste(out, input, sep = sep)
}
letters |> accumulate(paste3)

# Here the early return branch checks the incoming inputs passed on
# the RHS:
paste4 <- function(out, input, sep = ".") {
  if (input == "f") {
    return(done())
  }
  paste(out, input, sep = sep)
}
letters |> accumulate(paste4)


# Simulating stochastic processes with drift

library(dplyr)
library(ggplot2)

map(1:5, \(i) rnorm(100)) |>
  set_names(paste0("sim", 1:5)) |>
  map(\(l) accumulate(l, \(acc, nxt) .05 + acc + nxt)) |>
  map(\(x) tibble(value = x, step = 1:100)) |>
  list_rbind(names_to = "simulation") |>
  ggplot(aes(x = step, y = value)) +
    geom_line(aes(color = simulation)) +
    ggtitle("Simulations of a random walk with drift")