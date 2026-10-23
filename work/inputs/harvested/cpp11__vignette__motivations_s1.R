# r2py crawler metadata
# package: cpp11
# source_type: vignette
# topic: motivations_s1
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\cpp11\doc\motivations.R
# lines: 15

knitr::opts_chunk$set(
  collapse = TRUE,
  comment = "#>",
  eval = as.logical(Sys.getenv("CPP11_EVAL", "false"))
)

print_cpp <- function(filename) {
  cat("```c++", readLines(filename), "```", sep = "\n")
}

library(cpp11)

should_run_benchmarks <- function(x) {
  get("requireNamespace")("cpp11test", quietly = TRUE) && asNamespace("cpp11test")$should_run_benchmarks()
}