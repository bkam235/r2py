# r2py crawler metadata
# package: roxygen2
# source_type: vignette
# topic: extending_s19
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\roxygen2\doc\extending.R
# lines: 10

suppressPackageStartupMessages(library(roxygen2))
roclet_output.roclet_memo <- function(x, results, base_path, ...) {
  for (header in names(results)) {
    messages <- results[[header]]
    cat(paste0(header, ": ", "\n"))
    cat(paste0(" * ", messages, "\n", collapse = ""))
  }

  invisible(NULL)
}