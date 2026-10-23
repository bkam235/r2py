# r2py crawler metadata
# package: gitcreds
# source_type: vignette
# topic: package_s3
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\gitcreds\doc\package.R
# lines: 14

suppressPackageStartupMessages(library(gitcreds))
library(testthat)
test_that("another GitHub user", {
  cred <- paste0(
    "protocol:https:",
    "host:github.com:",
    "username:user1:",
    "password:secret"
  )
  withr::local_envvar(c(GITHUB_PAT_GITHUB_COM = cred))
  # Your test code comes here. This is just an illustration:
  print(gitcreds::gitcreds_get())
  expect_equal(gitcreds::gitcreds_get()$username, "user1")
})