# r2py crawler metadata
# package: recipes
# source_type: vignette
# topic: recipes_chunk1
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\recipes\doc\recipes.Rmd
# lines: 11

suppressPackageStartupMessages(library(recipes))
#| label: ex_setup
#| include: false
knitr::opts_chunk$set(
  message = FALSE,
  digits = 3,
  collapse = TRUE,
  comment = "#>",
  eval = requireNamespace("modeldata", quietly = TRUE) && requireNamespace("rsample", quietly = TRUE)
  )
options(digits = 3)