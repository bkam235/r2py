# r2py crawler metadata
# package: gargle
# source_type: vignette
# topic: troubleshooting_s5
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\gargle\doc\troubleshooting.R
# lines: 18

suppressPackageStartupMessages(library(gargle))
gargle_verbosity()

with_gargle_verbosity(
  "debug",
  gargle_verbosity()
)

gargle_verbosity()

f <- function() {
  local_gargle_verbosity("debug")
  gargle_verbosity()
}

f()

gargle_verbosity()