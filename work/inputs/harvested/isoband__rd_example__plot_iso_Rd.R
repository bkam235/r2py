# r2py crawler metadata
# package: isoband
# source_type: rd_example
# topic: plot_iso.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\isoband\help
# lines: 9

suppressPackageStartupMessages(library(isoband))
m <- matrix(c(0, 0, 0, 0, 0, 0,
              0, 2, 2, 2, 2, 0,
              0, 2, 0, 0, 2, 0,
              0, 2, 0, 0, 2, 0,
              0, 2, 2, 2, 2, 0,
              0, 0, 0, 0, 0, 0), 6, 6, byrow = TRUE)

plot_iso(m, 0.5, 1.5)