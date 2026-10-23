# r2py crawler metadata
# package: tibble
# source_type: vignette
# topic: numbers_s5
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\tibble\doc\numbers.R
# lines: 10

suppressPackageStartupMessages(library(tibble))
library(dplyr, warn.conflicts = FALSE)

markets <-
  as_tibble(EuStockMarkets) %>%
  mutate(time = time(EuStockMarkets), .before = 1)

markets
markets %>%
  mutate(across(-time, ~ num(.x, digits = 3)))