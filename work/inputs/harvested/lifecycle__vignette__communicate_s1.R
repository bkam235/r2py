# r2py crawler metadata
# package: lifecycle
# source_type: vignette
# topic: communicate_s1
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\lifecycle\doc\communicate.R
# lines: 12

suppressPackageStartupMessages(library(lifecycle))
knitr::opts_chunk$set(
  collapse = TRUE,
  comment = "#>"
)

options(
  # Pretend we're in the lifecycle package
  "lifecycle:::calling_package" = "lifecycle",
  # suppress last_lifecycle_warnings() message by default
  "lifecycle_verbosity" = "warning"
)