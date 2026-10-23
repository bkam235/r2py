# r2py crawler metadata
# package: gert
# source_type: vignette
# topic: gert_s1
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\gert\doc\gert.R
# lines: 11

suppressPackageStartupMessages(library(gert))
knitr::opts_chunk$set(
  collapse = TRUE,
  comment = "#>",
  error = TRUE
)

if (identical(Sys.getenv("IN_PKGDOWN"), "true") &&
    !gert:::global_user_is_configured()) {
  gert:::configure_global_user()
}