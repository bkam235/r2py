# r2py crawler metadata
# package: testthat
# source_type: vignette
# topic: third-edition_s10
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\testthat\doc\third-edition.R
# lines: 12

suppressPackageStartupMessages(library(testthat))
try({
dt1 <- dt2 <- ISOdatetime(2020, 1, 2, 3, 4, 0)
attr(dt1, "tzone") <- ""
attr(dt2, "tzone") <- Sys.timezone()

local_edition(2)
expect_equal(dt1, dt2)

local_edition(3)
expect_equal(dt1, dt2)
})