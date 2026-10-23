# r2py crawler metadata
# package: broom
# source_type: rd_example
# topic: glance.rma.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\broom\help
# lines: 19

suppressPackageStartupMessages(library(broom))
if (rlang::is_installed("metafor")) withAutoprint({ # examplesIf

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

glance(meta_analysis)
}) # examplesIf