# r2py crawler metadata
# package: broom
# source_type: rd_example
# topic: metafor_tidiers.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\broom\help
# lines: 20

suppressPackageStartupMessages(library(broom))
if (rlang::is_installed("metafor")) withAutoprint({ # examplesIf

# load libraries for models and data
library(metafor)

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

tidy(meta_analysis)
}) # examplesIf