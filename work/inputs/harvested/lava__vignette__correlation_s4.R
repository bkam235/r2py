# r2py crawler metadata
# package: lava
# source_type: vignette
# topic: correlation_s4
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\lava\doc\correlation.R
# lines: 4

suppressPackageStartupMessages(library(lava))
m0 <- lvm() |>
  covariance(y1 ~ y2, value='r') |>
  regression(y1 + y2 ~ x)