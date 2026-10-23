# r2py crawler metadata
# package: broom
# source_type: vignette
# topic: broom_chunk6
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\broom\doc\broom.Rmd
# lines: 6

suppressPackageStartupMessages(library(broom))
#| label: glmfit
glmfit <- glm(am ~ wt, mtcars, family = "binomial")
tidy(glmfit)
augment(glmfit)
glance(glmfit)