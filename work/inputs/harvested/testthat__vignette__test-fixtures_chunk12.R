# r2py crawler metadata
# package: testthat
# source_type: vignette
# topic: test-fixtures_chunk12
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\testthat\doc\test-fixtures.Rmd
# lines: 8

suppressPackageStartupMessages(library(testthat))
withr::defer(print("hi"))
#> Setting deferred event(s) on global environment.
#>   * Execute (and clear) with `deferred_run()`.
#>   * Clear (without executing) with `deferred_clear()`.

withr::deferred_run()
#> [1] "hi"