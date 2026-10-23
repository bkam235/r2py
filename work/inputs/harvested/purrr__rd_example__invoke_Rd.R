# r2py crawler metadata
# package: purrr
# source_type: rd_example
# topic: invoke.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\purrr\help
# lines: 34

suppressPackageStartupMessages(library(purrr))
# was
invoke(runif, list(n = 10))
invoke(runif, n = 10)
# now
exec(runif, n = 10)

# was
args <- list("01a", "01b")
invoke(paste, args, sep = "-")
# now
exec(paste, !!!args, sep = "-")

# was
funs <- list(runif, rnorm)
funs |> invoke_map(n = 5)
funs |> invoke_map(list(list(n = 10), list(n = 5)))

# now
funs |> map(exec, n = 5)
funs |> map2(list(list(n = 10), list(n = 5)), function(f, args) exec(f, !!!args))

# or use pmap + a tibble
df <- tibble::tibble(
  fun = list(runif, rnorm),
  args = list(list(n = 10), list(n = 5))
)
df |> pmap(function(fun, args) exec(fun, !!!args))


# was
list(m1 = mean, m2 = median) |> invoke_map(x = rcauchy(100))
# now
list(m1 = mean, m2 = median) |> map(function(f) f(rcauchy(100)))