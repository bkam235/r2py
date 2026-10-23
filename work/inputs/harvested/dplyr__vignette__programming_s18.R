# r2py crawler metadata
# package: dplyr
# source_type: vignette
# topic: programming_s18
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\doc\programming.R
# lines: 10

suppressPackageStartupMessages(library(dplyr))
quantile_df <- function(x, probs = c(0.25, 0.5, 0.75)) {
  tibble(
    val = quantile(x, probs),
    quant = probs
  )
}

x <- 1:5
quantile_df(x)