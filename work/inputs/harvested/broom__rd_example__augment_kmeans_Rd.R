# r2py crawler metadata
# package: broom
# source_type: rd_example
# topic: augment.kmeans.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\broom\help
# lines: 17

suppressPackageStartupMessages(library(broom))
if (FALSE) withAutoprint({ # examplesIf

library(cluster)
library(modeldata)
library(dplyr)

data(hpc_data)

x <- hpc_data[, 2:5]

fit <- pam(x, k = 4)

tidy(fit)
glance(fit)
augment(fit, x)
}) # examplesIf