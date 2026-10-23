# r2py crawler metadata
# package: broom
# source_type: rd_example
# topic: tidy.kde.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\broom\help
# lines: 34

suppressPackageStartupMessages(library(broom))
if (rlang::is_installed(c("ks", "ggplot2"))) withAutoprint({ # examplesIf

# load libraries for models and data
library(ks)

# generate data
dat <- replicate(2, rnorm(100))
k <- kde(dat)

# summarize model fit with tidiers + visualization
td <- tidy(k)
td

library(ggplot2)
library(dplyr)
library(tidyr)

td |>
  pivot_wider(c(obs, estimate),
    names_from = variable,
    values_from = value
  ) |>
  ggplot(aes(x1, x2, fill = estimate)) +
  geom_tile() +
  theme_void()

# also works with 3 dimensions
dat3 <- replicate(3, rnorm(100))
k3 <- kde(dat3)

td3 <- tidy(k3)
td3
}) # examplesIf