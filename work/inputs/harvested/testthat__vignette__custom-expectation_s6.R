# r2py crawler metadata
# package: testthat
# source_type: vignette
# topic: custom-expectation_s6
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\testthat\doc\custom-expectation.R
# lines: 7

suppressPackageStartupMessages(library(testthat))
test_that("mtcars is a 13 row data frame", {
  mtcars |>
    expect_type("list") |>
    expect_s3_class("data.frame") |> 
    expect_length(11)
})