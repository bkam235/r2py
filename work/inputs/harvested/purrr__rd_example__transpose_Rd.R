# r2py crawler metadata
# package: purrr
# source_type: rd_example
# topic: transpose.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\purrr\help
# lines: 35

suppressPackageStartupMessages(library(purrr))
x <- map(1:5, \(i) list(x = runif(1), y = runif(5)))
# was
x |> transpose() |> str()
# now
x |> list_transpose(simplify = FALSE) |> str()

# transpose() is useful in conjunction with safely() & quietly()
x <- list("a", 1, 2)
y <- x |> map(safely(log))
# was
y |> transpose() |> str()
# now:
y |> list_transpose() |> str()

# Previously, output simplification required a call to another function
x <- list(list(a = 1, b = 2), list(a = 3, b = 4), list(a = 5, b = 6))
x |> transpose() |> simplify_all()
# Now can take advantage of automatic simplification
x |> list_transpose()

# Provide explicit component names to prevent loss of those that don't
# appear in first component
ll <- list(
  list(x = 1, y = "one"),
  list(z = "deux", x = 2)
)
ll |> transpose()
nms <- ll |> map(names) |> reduce(union)
# was
ll |> transpose(.names = nms)
# now
ll |> list_transpose(template = nms)
# and can supply default value
ll |> list_transpose(template = nms, default = NA)