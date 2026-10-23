# r2py crawler metadata
# package: gitcreds
# source_type: vignette
# topic: package_s4
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\gitcreds\doc\package.R
# lines: 11

suppressPackageStartupMessages(library(gitcreds))
library(testthat)
test_that("no credentials from git", {
  withr::local_envvar(c(GITHUB_PAT_GITHUB_COM = "FAIL"))
  # The test code that calls gitcreds_get() comes here.
  # It will fail with error "gitcreds_no_credentials"
  expect_error(
    gitcreds::gitcreds_get("https://github.com"),
    class = "gitcreds_no_credentials"
  )
})