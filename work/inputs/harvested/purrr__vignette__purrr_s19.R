# r2py crawler metadata
# package: purrr
# source_type: vignette
# topic: purrr_s19
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\purrr\doc\purrr.R
# lines: 16

suppressPackageStartupMessages(library(purrr))
x <- list(
  a = letters[1:10],
  b = 1:10,
  c = runif(15)
)

x |> detect(is.character)
x |> detect_index(is.numeric)

x |> keep(is.numeric) |> str()
x |> discard(is.numeric) |> str()

x |> every(\(x) length(x) > 10)
x |> some(\(x) length(x) > 10)
x |> none(\(x) length(x) == 0)