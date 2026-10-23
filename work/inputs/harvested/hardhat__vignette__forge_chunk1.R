# r2py crawler metadata
# package: hardhat
# source_type: vignette
# topic: forge_chunk1
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\hardhat\doc\forge.Rmd
# lines: 15

suppressPackageStartupMessages(library(hardhat))
#| include: false
if (rlang::is_installed(c("modeldata", "recipes", "Matrix"))) {
  run <- TRUE
} else {
  run <- FALSE
}

knitr::opts_chunk$set(
  collapse = TRUE,
  comment = "#>",
  eval = run
)

options(rlang_backtrace_on_error = "none")