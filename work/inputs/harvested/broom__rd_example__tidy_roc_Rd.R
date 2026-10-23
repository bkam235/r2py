# r2py crawler metadata
# package: broom
# source_type: rd_example
# topic: tidy.roc.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\broom\help
# lines: 37

suppressPackageStartupMessages(library(broom))
if (rlang::is_installed(c("AUC", "ggplot2"))) withAutoprint({ # examplesIf

# load libraries for models and data
library(AUC)

# load data
data(churn)

# fit model
r <- roc(churn$predictions, churn$labels)

# summarize with tidiers + visualization
td <- tidy(r)
td

library(ggplot2)

ggplot(td, aes(fpr, tpr)) +
  geom_line()

# compare the ROC curves for two prediction algorithms
library(dplyr)
library(tidyr)

rocs <- churn |>
  pivot_longer(contains("predictions"),
    names_to = "algorithm",
    values_to = "value"
  ) |>
  nest(data = -algorithm) |>
  mutate(tidy_roc = purrr::map(data, \(x) tidy(roc(x$value, x$labels)))) |>
  unnest(tidy_roc)

ggplot(rocs, aes(fpr, tpr, color = algorithm)) +
  geom_line()
}) # examplesIf