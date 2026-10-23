# r2py crawler metadata
# package: isoband
# source_type: vignette
# topic: isoband1_s5
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\isoband\doc\isoband1.R
# lines: 9

suppressPackageStartupMessages(library(isoband))
m <- matrix(
  c(0, 0, 1, 1,
    0, 1, 1, 1,
    1, 1, 0, 0,
    0, 0, 0.8, 0),
  4, 4, byrow = TRUE
)
plot_iso(m, 0.5, 1.5)