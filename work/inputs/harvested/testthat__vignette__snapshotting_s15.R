# r2py crawler metadata
# package: testthat
# source_type: vignette
# topic: snapshotting_s15
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\testthat\doc\snapshotting.R
# lines: 11

suppressPackageStartupMessages(library(testthat))
safe_write_lines <- function(lines, path, overwrite = FALSE) {
  if (file.exists(path) && !overwrite) {
    cli::cli_abort(c(
      "{.path {path}} already exists.", 
      i = "Set {.code overwrite = TRUE} to overwrite"
    ))
  }

  writeLines(lines, path)
}