# r2py crawler metadata
# package: forcats
# source_type: rd_example
# topic: fct_lump.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\forcats\help
# lines: 40

suppressPackageStartupMessages(library(forcats))
x <- factor(rep(LETTERS[1:9], times = c(40, 10, 5, 27, 1, 1, 1, 1, 1)))
x |> table()
x |>
  fct_lump_n(3) |>
  table()
x |>
  fct_lump_prop(0.10) |>
  table()
x |>
  fct_lump_min(5) |>
  table()
x |>
  fct_lump_lowfreq() |>
  table()

x <- factor(letters[rpois(100, 5)])
x
table(x)
table(fct_lump_lowfreq(x))

# Use positive values to collapse the rarest
fct_lump_n(x, n = 3)
fct_lump_prop(x, prop = 0.1)

# Use negative values to collapse the most common
fct_lump_n(x, n = -3)
fct_lump_prop(x, prop = -0.1)

# Use weighted frequencies
w <- c(rep(2, 50), rep(1, 50))
fct_lump_n(x, n = 5, w = w)

# Use ties.method to control how tied factors are collapsed
fct_lump_n(x, n = 6)
fct_lump_n(x, n = 6, ties.method = "max")

# Use fct_lump_min() to lump together all levels with fewer than `n` values
table(fct_lump_min(x, min = 10))
table(fct_lump_min(x, min = 15))