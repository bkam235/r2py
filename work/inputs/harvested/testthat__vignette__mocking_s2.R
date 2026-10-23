# r2py crawler metadata
# package: testthat
# source_type: vignette
# topic: mocking_s2
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\testthat\doc\mocking.R
# lines: 19

suppressPackageStartupMessages(library(testthat))
check_installed <- function(pkg, min_version = NULL) {
  if (!requireNamespace(pkg, quietly = TRUE)) {
    stop(sprintf("{%s} is not installed.", pkg))
  }
  if (!is.null(min_version)) {
    pkg_version <- packageVersion(pkg)
    if (pkg_version < min_version) {
      stop(sprintf(
        "{%s} version %s is installed, but %s is required.", 
        pkg, 
        pkg_version, 
        min_version
      ))
    }
  }

  invisible()
}