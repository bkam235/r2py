# r2py crawler metadata
# package: broom
# source_type: rd_example
# topic: glance.multinom.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\broom\help
# lines: 19

suppressPackageStartupMessages(library(broom))
if (rlang::is_installed(c("nnet", "MASS"))) withAutoprint({ # examplesIf

# load libraries for models and data
library(nnet)
library(MASS)

example(birthwt)

bwt.mu <- multinom(low ~ ., bwt)

tidy(bwt.mu)
glance(bwt.mu)

# or, for output from a multinomial logistic regression
fit.gear <- multinom(gear ~ mpg + factor(am), data = mtcars)
tidy(fit.gear)
glance(fit.gear)
}) # examplesIf