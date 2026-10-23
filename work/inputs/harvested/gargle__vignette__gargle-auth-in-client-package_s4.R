# r2py crawler metadata
# package: gargle
# source_type: vignette
# topic: gargle-auth-in-client-package_s4
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\gargle\doc\gargle-auth-in-client-package.R
# lines: 9

suppressPackageStartupMessages(library(gargle))
.onLoad <- function(libname, pkgname) {
  utils::assignInMyNamespace(
    ".auth",
    gargle::init_AuthState(package = "googledrive", auth_active = TRUE)
  )
  
  # other stuff
}