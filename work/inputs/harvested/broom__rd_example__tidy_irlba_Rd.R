# r2py crawler metadata
# package: broom
# source_type: rd_example
# topic: tidy_irlba.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\broom\help
# lines: 31

suppressPackageStartupMessages(library(broom))
if (rlang::is_installed(c("modeldata", "ggplot2"))) withAutoprint({ # examplesIf

library(modeldata)
data(hpc_data)

mat <- scale(as.matrix(hpc_data[, 2:5]))
s <- svd(mat)

tidy_u <- tidy(s, matrix = "u")
tidy_u

tidy_d <- tidy(s, matrix = "d")
tidy_d

tidy_v <- tidy(s, matrix = "v")
tidy_v

library(ggplot2)
library(dplyr)

ggplot(tidy_d, aes(PC, percent)) +
  geom_point() +
  ylab("% of variance explained")

tidy_u |>
  mutate(class = hpc_data$class[row]) |>
  ggplot(aes(class, value)) +
  geom_boxplot() +
  facet_wrap(~PC, scale = "free_y")
}) # examplesIf