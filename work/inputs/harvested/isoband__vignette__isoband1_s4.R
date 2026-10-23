# r2py crawler metadata
# package: isoband
# source_type: vignette
# topic: isoband1_s4
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\isoband\doc\isoband1.R
# lines: 11

suppressPackageStartupMessages(library(isoband))
m <- matrix(
  c(NA, NA, NA, 0, 0, 0,
    NA, NA, NA, 1, 1, 0,
     0,  0,  1, 1, 1, 0,
     0,  1,  1, 0, 0, 0,
     0,  0,  0, 1, 0, 0,
     0,  0,  0, 0, 0, 0),
  6, 6, byrow = TRUE
)
plot_iso(m, 0.5, 1.5)