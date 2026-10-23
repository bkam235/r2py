# r2py crawler metadata
# package: purrr
# source_type: rd_example
# topic: map2.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\purrr\help
# lines: 12

suppressPackageStartupMessages(library(purrr))
x <- list(1, 1, 1)
y <- list(10, 20, 30)

map2(x, y, \(x, y) x + y)
# Or just
map2(x, y, `+`)

# Split into pieces, fit model to each piece, then predict
by_cyl <- mtcars |> split(mtcars$cyl)
mods <- by_cyl |> map(\(df) lm(mpg ~ wt, data = df))
map2(mods, by_cyl, predict)