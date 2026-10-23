# r2py crawler metadata
# package: highr
# source_type: vignette
# topic: highr-custom_s2
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\highr\doc\highr-custom.R
# lines: 4

suppressPackageStartupMessages(library(highr))
m = highr:::cmd_latex
m[, 1] = sub('\\hl', '\\my', m[, 1], fixed = TRUE)
head(m)