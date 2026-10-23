# r2py crawler metadata
# package: testthat
# source_type: vignette
# topic: custom-expectation_s10
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\testthat\doc\custom-expectation.R
# lines: 5

suppressPackageStartupMessages(library(testthat))
try({
expect_vector_length(mean, 1)
expect_vector_length(mtcars, 15)
})