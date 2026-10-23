# r2py crawler metadata
# package: hardhat
# source_type: vignette
# topic: forge_s1
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\hardhat\doc\forge.R
# lines: 14

suppressPackageStartupMessages(library(hardhat))
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