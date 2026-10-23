# r2py crawler metadata
# package: gargle
# source_type: vignette
# topic: troubleshooting_s4
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\gargle\doc\troubleshooting.R
# lines: 8

suppressPackageStartupMessages(library(gargle))
# save current value
op <- options(gargle_verbosity = "debug")

gargle_verbosity()

# restore original value
options(op)