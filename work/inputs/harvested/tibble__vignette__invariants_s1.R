# r2py crawler metadata
# package: tibble
# source_type: vignette
# topic: invariants_s1
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\tibble\doc\invariants.R
# lines: 20

# To suppress messages
library(tibble)
library(vctrs)

knitr::opts_chunk$set(
  collapse = TRUE,
  comment = "#>",
  error = TRUE
)
tibble:::set_dftbl_hooks()

options(
  lifecycle_verbosity = "warning",
  lifecycle_disable_warnings = FALSE,
  lifecycle_verbose_soft_deprecation = TRUE,
  lifecycle_repeat_warnings = TRUE
)

# Set to FALSE for production
eval_details <- (Sys.getenv("IN_GALLEY") != "")