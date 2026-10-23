# r2py crawler metadata
# package: purrr
# source_type: vignette
# topic: purrr_s10
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\purrr\doc\purrr.R
# lines: 9

suppressPackageStartupMessages(library(purrr))
try({
my_lm <- function(formula, data) {
  Sys.sleep(0.5)
  lm(formula, data)
}
by_cyl <- split(mtcars, mtcars$cyl)
out <- map(by_cyl, in_parallel(\(df) my_lm(mpg ~ disp, data = df)))
})