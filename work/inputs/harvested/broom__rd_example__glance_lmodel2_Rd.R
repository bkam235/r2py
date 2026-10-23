# r2py crawler metadata
# package: broom
# source_type: rd_example
# topic: glance.lmodel2.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\broom\help
# lines: 22

suppressPackageStartupMessages(library(broom))
if (rlang::is_installed(c("lmodel2", "ggplot2"))) withAutoprint({ # examplesIf

# load libraries for models and data
library(lmodel2)

data(mod2ex2)
Ex2.res <- lmodel2(Prey ~ Predators, data = mod2ex2, "relative", "relative", 99)
Ex2.res

# summarize model fit with tidiers + visualization
tidy(Ex2.res)
glance(Ex2.res)

# this allows coefficient plots with ggplot2
library(ggplot2)

ggplot(tidy(Ex2.res), aes(estimate, term, color = method)) +
  geom_point() +
  geom_errorbarh(aes(xmin = conf.low, xmax = conf.high)) +
  geom_errorbarh(aes(xmin = conf.low, xmax = conf.high))
}) # examplesIf