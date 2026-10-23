# r2py crawler metadata
# package: purrr
# source_type: rd_example
# topic: rerun.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\purrr\help
# lines: 14

suppressPackageStartupMessages(library(purrr))
# old
5 |> rerun(rnorm(5)) |> str()
# new
1:5 |> map(\(i) rnorm(5)) |> str()

# old
5 |>
  rerun(x = rnorm(5), y = rnorm(5)) |>
  map_dbl(\(l) cor(l$x, l$y))
# new
1:5 |>
  map(\(i) list(x = rnorm(5), y = rnorm(5))) |>
  map_dbl(\(l) cor(l$x, l$y))