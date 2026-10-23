# r2py crawler metadata
# package: testthat
# source_type: vignette
# topic: third-edition_s9
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\testthat\doc\third-edition.R
# lines: 11

suppressPackageStartupMessages(library(testthat))
try({
f1 <- factor(letters[1:3])
f2 <- ordered(letters[1:3], levels = letters[1:4])

local_edition(2)
expect_equal(f1, f2)

local_edition(3)
expect_equal(f1, f2)
})