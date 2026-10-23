# r2py crawler metadata
# package: broom
# source_type: rd_example
# topic: augment.pam.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\broom\help
# lines: 23

suppressPackageStartupMessages(library(broom))
if (rlang::is_installed(c("cluster", "modeldata", "ggplot2")) && identical(Sys.getenv("NOT_CRAN"), "true")) withAutoprint({ # examplesIf

# load libraries for models and data
library(dplyr)
library(ggplot2)
library(cluster)
library(modeldata)
data(hpc_data)

x <- hpc_data[, 2:5]
p <- pam(x, k = 4)

# summarize model fit with tidiers + visualization
tidy(p)
glance(p)
augment(p, x)

augment(p, x) |>
  ggplot(aes(compounds, input_fields)) +
  geom_point(aes(color = .cluster)) +
  geom_text(aes(label = cluster), data = tidy(p), size = 10)
}) # examplesIf