# r2py crawler metadata
# package: fansi
# source_type: vignette
# topic: sgr-in-rmd_s2
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\fansi\doc\sgr-in-rmd.R
# lines: 6

suppressPackageStartupMessages(library(fansi))
sgr.string <- c(
  "\033[43;34mday > night\033[0m",
  "\033[44;33mdawn < dusk\033[0m"
)
writeLines(sgr.string)