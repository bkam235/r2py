# r2py crawler metadata
# package: lava
# source_type: vignette
# topic: nonlinear_s1
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\lava\doc\nonlinear.R
# lines: 7

suppressPackageStartupMessages(library(lava))
knitr::opts_chunk$set(
  collapse = TRUE,
  comment = "#>"
)
mets <- lava:::versioncheck('mets', 1)
fullVignette <- Sys.getenv("_R_FULL_VIGNETTE_") %in% c("1","TRUE")