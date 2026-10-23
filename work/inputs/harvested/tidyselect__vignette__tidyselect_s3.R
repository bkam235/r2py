# r2py crawler metadata
# package: tidyselect
# source_type: vignette
# topic: tidyselect_s3
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\tidyselect\doc\tidyselect.R
# lines: 9

suppressPackageStartupMessages(library(tidyselect))
# For better printing
mtcars <- tibble::as_tibble(mtcars)
iris <- tibble::as_tibble(iris)

options(
  tibble.print_min = 4,
  tibble.print_max = 4
)