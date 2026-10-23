# r2py crawler metadata
# package: tibble
# source_type: vignette
# topic: invariants_chunk2
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\tibble\doc\invariants.Rmd
# lines: 14

#| label: setup
library(tibble)
library(vctrs)

new_df <- function() {
  df <- data.frame(n = c(1L, NA, 3L, NA))
  df$c <- letters[5:8]
  df$li <- list(9, 10:11, 12:14, "text")
  df
}

new_tbl <- function() {
  as_tibble(new_df())
}