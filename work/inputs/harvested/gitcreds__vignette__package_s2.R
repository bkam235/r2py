# r2py crawler metadata
# package: gitcreds
# source_type: vignette
# topic: package_s2
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\gitcreds\doc\package.R
# lines: 12

suppressPackageStartupMessages(library(gitcreds))
library(testthat)
test_that("bad credentials from git", {
  withr::local_envvar(c(GITHUB_PAT_GITHUB_COM = "bad"))
  # Test code that calls gitcreds_get(), potentially downstream.
  # gitcreds_get() will return `bad` as the password.
  # Illustration:
  expect_equal(
    gitcreds::gitcreds_get("https://github.com")$password,
    "bad"
  )
})