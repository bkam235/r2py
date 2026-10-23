# r2py crawler metadata
# package: broom
# source_type: rd_example
# topic: tidy.lm.beta.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\broom\help
# lines: 26

suppressPackageStartupMessages(library(broom))
if (rlang::is_installed("lm.beta")) withAutoprint({ # examplesIf

# load libraries for models and data
library(lm.beta)

# fit models
mod <- stats::lm(speed ~ ., data = cars)
std <- lm.beta(mod)

# summarize model fit with tidiers
tidy(std, conf.int = TRUE)

# generate data
ctl <- c(4.17, 5.58, 5.18, 6.11, 4.50, 4.61, 5.17, 4.53, 5.33, 5.14)
trt <- c(4.81, 4.17, 4.41, 3.59, 5.87, 3.83, 6.03, 4.89, 4.32, 4.69)
group <- gl(2, 10, 20, labels = c("Ctl", "Trt"))
weight <- c(ctl, trt)

# fit models
mod2 <- lm(weight ~ group)
std2 <- lm.beta(mod2)

# summarize model fit with tidiers
tidy(std2, conf.int = TRUE)
}) # examplesIf