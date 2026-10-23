# r2py crawler metadata
# package: roxygen2
# source_type: vignette
# topic: extending_s11
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\roxygen2\doc\extending.R
# lines: 10

suppressPackageStartupMessages(library(roxygen2))
format.rd_section_tip <- function(x, ...) {
  paste0(
    "\\section{Tips and tricks}{\n",
    "\\itemize{\n",
    paste0("  \\item ", x$value, "\n", collapse = ""),
    "}\n",
    "}\n"
  )
}