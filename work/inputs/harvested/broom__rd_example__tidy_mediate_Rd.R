# r2py crawler metadata
# package: broom
# source_type: rd_example
# topic: tidy.mediate.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\broom\help
# lines: 18

suppressPackageStartupMessages(library(broom))
if (rlang::is_installed("mediation")) withAutoprint({ # examplesIf

# load libraries for models and data
library(mediation)

data("jobs", package = "mediation")

# fit models
b <- lm(job_seek ~ treat + econ_hard + sex + age, data = jobs)
c <- lm(depress2 ~ treat + job_seek + econ_hard + sex + age, data = jobs)
mod <- mediate(b, c, sims = 50, treat = "treat", mediator = "job_seek")

# summarize model fit with tidiers
tidy(mod)
tidy(mod, conf.int = TRUE)
tidy(mod, conf.int = TRUE, conf.level = .99)
}) # examplesIf