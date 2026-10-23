# r2py crawler metadata
# package: broom
# source_type: vignette
# topic: broom_s6
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\broom\doc\broom.R
# lines: 5

suppressPackageStartupMessages(library(broom))
glmfit <- glm(am ~ wt, mtcars, family = "binomial")
tidy(glmfit)
augment(glmfit)
glance(glmfit)