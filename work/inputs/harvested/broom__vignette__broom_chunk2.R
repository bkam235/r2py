# r2py crawler metadata
# package: broom
# source_type: vignette
# topic: broom_chunk2
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\broom\doc\broom.Rmd
# lines: 5

suppressPackageStartupMessages(library(broom))
#| label: lmfit
lmfit <- lm(mpg ~ wt, mtcars)
lmfit
summary(lmfit)