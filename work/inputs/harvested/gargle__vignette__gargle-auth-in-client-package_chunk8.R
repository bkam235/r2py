# r2py crawler metadata
# package: gargle
# source_type: vignette
# topic: gargle-auth-in-client-package_chunk8
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\gargle\doc\gargle-auth-in-client-package.Rmd
# lines: 9

suppressPackageStartupMessages(library(gargle))
#| eval: false
# googledrive::
drive_auth <- function(email = gargle::gargle_oauth_email(),
                       path = NULL,
                       scopes = "https://www.googleapis.com/auth/drive",
                       cache = gargle::gargle_oauth_cache(),
                       use_oob = gargle::gargle_oob_default(),
                       token = NULL) { ... }