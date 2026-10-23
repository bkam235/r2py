# r2py crawler metadata
# package: testthat
# source_type: vignette
# topic: custom-expectation_chunk1
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\testthat\doc\custom-expectation.Rmd
# lines: 7

#| include: false
library(testthat)
knitr::opts_chunk$set(collapse = TRUE, comment = "#>")

# Pretend we're snapshotting
snapper <- local_snapshotter(fail_on_new = FALSE)
snapper$start_file("snapshotting.Rmd", "test")