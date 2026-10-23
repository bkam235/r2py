# r2py crawler metadata
# package: glue
# source_type: vignette
# topic: glue_s7
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\glue\doc\glue.R
# lines: 8

suppressPackageStartupMessages(library(glue))
foo <- function() {
  glue("
    A formatted string
    Can have multiple lines
      with additional indention preserved")
}
foo()