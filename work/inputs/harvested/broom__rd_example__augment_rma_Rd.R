# r2py crawler metadata
# package: broom
# source_type: rd_example
# topic: augment.rma.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\broom\help
# lines: 22

suppressPackageStartupMessages(library(broom))
if (rlang::is_installed("metafor")) withAutoprint({ # examplesIf

# load modeling library
library(metafor)

# generate data and fit
df <-
  escalc(
    measure = "RR",
    ai = tpos,
    bi = tneg,
    ci = cpos,
    di = cneg,
    data = dat.bcg
  )

meta_analysis <- rma(yi, vi, data = df, method = "EB")

# summarize model fit with tidiers
augment(meta_analysis)
}) # examplesIf