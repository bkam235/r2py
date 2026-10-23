# r2py crawler metadata
# package: gitcreds
# source_type: vignette
# topic: package_s5
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\gitcreds\doc\package.R
# lines: 13

suppressPackageStartupMessages(library(gitcreds))
library(testthat)
test_that("no git installation", {
  withr::local_envvar(c(
    GITHUB_PAT_GITHUB_COM = "FAIL:gitcreds_nogit_error"
  ))
  # Test code that calls gitcreds_get() comes here.
  # Illustration:
  expect_error(
    gitcreds::gitcreds_get("https://github.com"),
    class = "gitcreds_nogit_error"
  )
})