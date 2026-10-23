# r2py crawler metadata
# package: tibble
# source_type: vignette
# topic: numbers_chunk5
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\tibble\doc\numbers.Rmd
# lines: 11

suppressPackageStartupMessages(library(tibble))
#| eval: !expr rlang::is_installed("dplyr")
library(dplyr, warn.conflicts = FALSE)

markets <-
  as_tibble(EuStockMarkets) %>%
  mutate(time = time(EuStockMarkets), .before = 1)

markets
markets %>%
  mutate(across(-time, ~ num(.x, digits = 3)))