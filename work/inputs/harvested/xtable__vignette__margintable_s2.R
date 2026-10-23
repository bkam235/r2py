# r2py crawler metadata
# package: xtable
# source_type: vignette
# topic: margintable_s2
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xtable\doc\margintable.R
# lines: 3

library(xtable)
x <- matrix(rnorm(6), ncol = 2)
x.small <- xtable(x, label = 'tabsmall', caption = 'A margin table')