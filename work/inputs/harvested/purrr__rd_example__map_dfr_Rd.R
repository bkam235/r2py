# r2py crawler metadata
# package: purrr
# source_type: rd_example
# topic: map_dfr.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\purrr\help
# lines: 50

suppressPackageStartupMessages(library(purrr))
# map ---------------------------------------------
# Was:
mtcars |>
  split(mtcars$cyl) |>
  map(\(df) lm(mpg ~ wt, data = df)) |>
  map_dfr(\(mod) as.data.frame(t(as.matrix(coef(mod)))))

# Now:
mtcars |>
  split(mtcars$cyl) |>
  map(\(df) lm(mpg ~ wt, data = df)) |>
  map(\(mod) as.data.frame(t(as.matrix(coef(mod))))) |>
  list_rbind()

# for certain pathological inputs `map_dfr()` and `map_dfc()` actually
# both combine the list by column
df <- data.frame(
  x = c(" 13", "  15 "),
  y = c("  34",  " 67 ")
)

# Was:
map_dfr(df, trimws)
map_dfc(df, trimws)

# But list_rbind()/list_cbind() fail because they require data frame inputs
try(map(df, trimws) |> list_rbind())

# Instead, use modify() to apply a function to each column of a data frame
modify(df, trimws)

# map2 ---------------------------------------------

ex_fun <- function(arg1, arg2){
  col <- arg1 + arg2
  x <- as.data.frame(col)
}
arg1 <- 1:4
arg2 <- 10:13

# was
map2_dfr(arg1, arg2, ex_fun)
# now
map2(arg1, arg2, ex_fun) |> list_rbind()

# was
map2_dfc(arg1, arg2, ex_fun)
# now
map2(arg1, arg2, ex_fun) |> list_cbind()