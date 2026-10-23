# r2py crawler metadata
# package: broom
# source_type: rd_example
# topic: tidy.epi.2by2.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\broom\help
# lines: 22

suppressPackageStartupMessages(library(broom))
if (rlang::is_installed("epiR")) withAutoprint({ # examplesIf

# load libraries for models and data
library(epiR)

# generate data
dat <- matrix(c(13, 2163, 5, 3349), nrow = 2, byrow = TRUE)

rownames(dat) <- c("DF+", "DF-")
colnames(dat) <- c("FUS+", "FUS-")

# fit model
fit <- epi.2by2(
  dat = as.table(dat), method = "cross.sectional",
  conf.level = 0.95, units = 100, outcome = "as.columns"
)

# summarize model fit with tidiers
tidy(fit, parameters = "moa")
tidy(fit, parameters = "stat")
}) # examplesIf