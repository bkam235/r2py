# r2py crawler metadata
# package: backports
# source_type: rd_example
# topic: import.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\backports\help
# lines: 16

suppressPackageStartupMessages(library(backports))
# This imports all functions implemented in backports while the package is loaded
.onLoad <- function(libname, pkgname) {
  backports::import(pkgname)
}

# This only imports the function "trimws"
.onLoad <- function(libname, pkgname) {
  backports::import(pkgname, "trimws")
}

# This imports all backports from base and force-imports "hasName" from utils
.onLoad <- function(libname, pkgname) {
  backports::import(pkgname)
  backports::import(pkgname, "hasName", force = TRUE)
}