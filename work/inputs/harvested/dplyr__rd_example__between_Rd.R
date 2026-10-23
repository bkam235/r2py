# r2py crawler metadata
# package: dplyr
# source_type: rd_example
# topic: between.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\help
# lines: 17

suppressPackageStartupMessages(library(dplyr))
between(1:12, 7, 9)

x <- rnorm(1e2)
x[between(x, -1, 1)]

# On a tibble using `filter()`
filter(starwars, between(height, 100, 150))

# Using the `ptype` argument with ordered factors, where otherwise everything
# is cast to the common type of character before the comparison
x <- ordered(
  c("low", "medium", "high", "medium"),
  levels = c("low", "medium", "high")
)
between(x, "medium", "high")
between(x, "medium", "high", ptype = x)