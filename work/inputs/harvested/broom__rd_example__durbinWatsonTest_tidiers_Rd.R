# r2py crawler metadata
# package: broom
# source_type: rd_example
# topic: durbinWatsonTest_tidiers.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\broom\help
# lines: 15

suppressPackageStartupMessages(library(broom))
if (rlang::is_installed("car")) {
  withAutoprint({
    # examplesIf

    # load modeling library
    library(car)

    # fit model
    dw <- durbinWatsonTest(lm(mpg ~ wt, data = mtcars))

    # summarize model fit with tidiers
    tidy(dw)

    # same output for all durbinWatsonTests
    glance(dw)
  })
} # examplesIf
