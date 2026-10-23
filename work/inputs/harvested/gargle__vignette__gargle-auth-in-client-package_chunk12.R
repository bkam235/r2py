# r2py crawler metadata
# package: gargle
# source_type: vignette
# topic: gargle-auth-in-client-package_chunk12
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\gargle\doc\gargle-auth-in-client-package.Rmd
# lines: 6

suppressPackageStartupMessages(library(gargle))
#| eval: false
# googledrive::
drive_has_token <- function() {
  inherits(.auth$cred, "Token2.0")
}