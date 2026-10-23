# r2py crawler metadata
# package: purrr
# source_type: rd_example
# topic: reduce.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\purrr\help
# lines: 54

suppressPackageStartupMessages(library(purrr))
# Reducing `+` computes the sum of a vector while reducing `*`
# computes the product:
1:3 |> reduce(`+`)
1:10 |> reduce(`*`)

# By ignoring the input vector (nxt), you can turn output of one step into
# the input for the next. This code takes 10 steps of a random walk:
reduce(1:10, \(acc, nxt) acc + rnorm(1), .init = 0)

# When the operation is associative, the direction of reduction
# does not matter:
reduce(1:4, `+`)
reduce(1:4, `+`, .dir = "backward")

# However with non-associative operations, the reduced value will
# be different as a function of the direction. For instance,
# `list()` will create left-leaning lists when reducing from the
# right, and right-leaning lists otherwise:
str(reduce(1:4, list))
str(reduce(1:4, list, .dir = "backward"))

# reduce2() takes a ternary function and a second vector that is
# one element smaller than the first vector:
paste2 <- function(x, y, sep = ".") paste(x, y, sep = sep)
letters[1:4] |> reduce(paste2)
letters[1:4] |> reduce2(c("-", ".", "-"), paste2)

x <- list(c(0, 1), c(2, 3), c(4, 5))
y <- list(c(6, 7), c(8, 9))
reduce2(x, y, paste)


# You can shortcircuit a reduction and terminate it early by
# returning a value wrapped in a done(). In the following example
# we return early if the result-so-far, which is passed on the LHS,
# meets a condition:
paste3 <- function(out, input, sep = ".") {
  if (nchar(out) > 4) {
    return(done(out))
  }
  paste(out, input, sep = sep)
}
letters |> reduce(paste3)

# Here the early return branch checks the incoming inputs passed on
# the RHS:
paste4 <- function(out, input, sep = ".") {
  if (input == "j") {
    return(done(out))
  }
  paste(out, input, sep = sep)
}
letters |> reduce(paste4)