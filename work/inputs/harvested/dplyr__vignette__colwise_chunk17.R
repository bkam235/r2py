# r2py crawler metadata
# package: dplyr
# source_type: vignette
# topic: colwise_chunk17
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\doc\colwise.Rmd
# lines: 7

suppressPackageStartupMessages(library(dplyr))
rescale01 <- function(x) {
      rng <- range(x, na.rm = TRUE)
      (x - rng[1]) / (rng[2] - rng[1])
    }
    df <- tibble(x = 1:4, y = rnorm(4))
    df |> mutate(across(where(is.numeric), rescale01))