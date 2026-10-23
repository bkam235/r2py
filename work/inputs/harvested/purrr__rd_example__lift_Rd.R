# r2py crawler metadata
# package: purrr
# source_type: rd_example
# topic: lift.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\purrr\help
# lines: 40

suppressPackageStartupMessages(library(purrr))
### Lifting from ... to list(...) or c(...)

x <- list(x = c(1:100, NA, 1000), na.rm = TRUE, trim = 0.9)
lift_dl(mean)(x)
# You can also use the lift() alias for this common operation:
lift(mean)(x)
# now:
exec(mean, !!!x)

# Default arguments can also be specified directly in lift_dl()
list(c(1:100, NA, 1000)) |> lift_dl(mean, na.rm = TRUE)()
# now:
mean(c(1:100, NA, 1000), na.rm = TRUE)

# lift_dl() and lift_ld() are inverse of each other.
# Here we transform sum() so that it takes a list
fun <- sum |> lift_dl()
fun(list(3, NA, 4, na.rm = TRUE))
# now:
fun <- function(x) exec("sum", !!!x)
exec(sum, 3, NA, 4, na.rm = TRUE)
### Lifting from c(...) to list(...) or ...

# In other situations we need the vector-valued function to take a
# variable number of arguments as with pmap(). This is a job for
# lift_vd():
pmap_dbl(mtcars, lift_vd(mean))
# now
pmap_dbl(mtcars, \(...) mean(c(...)))
### Lifting from list(...) to c(...) or ...

# This kind of lifting is sometimes needed for function
# composition. An example would be to use pmap() with a function
# that takes a list. In the following, we use some() on each row of
# a data frame to check they each contain at least one element
# satisfying a condition:
mtcars |> pmap_lgl(lift_ld(some, partial(`<`, 200)))
# now
mtcars |> pmap_lgl(\(...) any(c(...) > 200))