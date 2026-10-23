# r2py crawler metadata
# package: knitr
# source_type: vignette
# topic: knitr-intro_chunk1
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\knitr\doc\knitr-intro.Rmd
# lines: 5

suppressPackageStartupMessages(library(knitr))
options(digits = 4)
rnorm(20)
fit = lm(dist ~ speed, data = cars)
b = coef(fit)