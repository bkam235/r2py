# r2py crawler metadata
# package: broom
# source_type: vignette
# topic: broom_s7
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\broom\doc\broom.R
# lines: 5

suppressPackageStartupMessages(library(broom))
nlsfit <- nls(mpg ~ k / wt + b, mtcars, start = list(k = 1, b = 0))
tidy(nlsfit)
augment(nlsfit, mtcars)
glance(nlsfit)