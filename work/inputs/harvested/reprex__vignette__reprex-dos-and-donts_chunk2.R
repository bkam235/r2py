# r2py crawler metadata
# package: reprex
# source_type: vignette
# topic: reprex-dos-and-donts_chunk2
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\reprex\doc\reprex-dos-and-donts.Rmd
# lines: 11

suppressPackageStartupMessages(library(reprex))
tibble::tribble(
        ~ a, ~ b,
          1,   2,
          3,   4
      )
      #> # A tibble: 2 x 2
      #>       a     b
      #>   <dbl> <dbl>
      #> 1     1     2
      #> 2     3     4