# r2py crawler metadata
# package: broom
# source_type: rd_example
# topic: tidy.mlm.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\broom\help
# lines: 6

suppressPackageStartupMessages(library(broom))
# fit model
mod <- lm(cbind(mpg, disp) ~ wt, mtcars)

# summarize model fit with tidiers
tidy(mod, conf.int = TRUE)