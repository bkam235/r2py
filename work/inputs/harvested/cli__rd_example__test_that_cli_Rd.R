# r2py crawler metadata
# package: cli
# source_type: rd_example
# topic: test_that_cli.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\cli\help
# lines: 30

suppressPackageStartupMessages(library(cli))
# testthat cannot record or compare snapshots when you run these
# examples interactively, so you might want to copy them into a test
# file

# Default configurations
cli::test_that_cli("success", {
  testthat::local_edition(3)
  testthat::expect_snapshot({
    cli::cli_alert_success("wow")
  })
})

# Only use two configurations, because this output does not have colors
cli::test_that_cli(configs = c("plain", "unicode"), "cat_bullet", {
  testthat::local_edition(3)
  testthat::expect_snapshot({
    cli::cat_bullet(letters[1:5])
  })
})

# You often need to evaluate all cli calls of a test case in the same
# environment. Use `local()` to do that:
cli::test_that_cli("theming", {
  testthat::local_edition(3)
  testthat::expect_snapshot(local({
    cli::cli_div(theme = list(".alert" = list(before = "!!! ")))
    cli::cli_alert("wow")
  }))
})