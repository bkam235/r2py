# r2py crawler metadata
# package: testthat
# source_type: vignette
# topic: challenging-tests_chunk1
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\testthat\doc\challenging-tests.Rmd
# lines: 10

#| include: false
library(testthat)
knitr::opts_chunk$set(collapse = TRUE, comment = "#>")

# Pretend we're snapshotting
snapper <- local_snapshotter(fail_on_new = FALSE)
snapper$start_file("snapshotting.Rmd", "test")

# Pretend we're testing testthat so we can use mocking
Sys.setenv(TESTTHAT_PKG = "testthat")